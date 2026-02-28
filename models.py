from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets

db = SQLAlchemy()

# Association table for Friendships
friendships = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
)

class Guild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    access_code = db.Column(db.String(10), unique=True, nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    members = db.relationship('User', foreign_keys='User.guild_id', backref='guild', lazy=True)
    leader = db.relationship('User', foreign_keys=[leader_id], backref='led_guilds', lazy=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # NEW: 6-digit hex code
    hex_code = db.Column(db.String(6), unique=True, nullable=False)
    
    # NEW: Guild ID
    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Points/Gamification
    total_points = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)

    # NEW: Friendships relationship
    friends = db.relationship('User', secondary=friendships,
                              primaryjoin=(friendships.c.user_id == id),
                              secondaryjoin=(friendships.c.friend_id == id),
                              backref=db.backref('friend_of', lazy='dynamic'), lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.hex_code:
            self.hex_code = secrets.token_hex(3).upper()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class AppUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    app_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # e.g., 'Social Media', 'Productivity', 'Entertainment'
    duration_minutes = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # The user requested logs every 3 hours. 
    # This interval_id can help group logs into 3-hour windows.
    # 0: 00-03, 1: 03-06, 2: 06-09, 3: 09-12, 4: 12-15, 5: 15-18, 6: 18-21, 7: 21-24
    interval_id = db.Column(db.Integer, nullable=False)  
