from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, AppUsage
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_hackathon_key'  # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dopamine_detox.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from analytics import get_behavioral_patterns, get_daily_trends

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    patterns = get_behavioral_patterns(current_user.id)
    trends = get_daily_trends(current_user.id)
    return render_template('dashboard.html', patterns=patterns, trends=trends, user=current_user)

@app.route('/api/stats')
@login_required
def get_stats():
    patterns = get_behavioral_patterns(current_user.id)
    return jsonify(patterns)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a default user if none exists
        if not User.query.first():
            default_user = User(username="default_user")
            db.session.add(default_user)
            db.session.commit()
            print("Default user created.")
    
    app.run(debug=True, port=5000)
