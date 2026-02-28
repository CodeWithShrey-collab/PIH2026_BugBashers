from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, AppUsage
from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from datetime import datetime
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
from intelligence import get_intelligence_data

def require_api_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
        token = auth_header.split(" ")[1]
        serializer = URLSafeTimedSerializer(app.secret_key)
        try:
            data = serializer.loads(token, max_age=86400 * 30) # 30 days
        except Exception:
            return jsonify({"error": "Token expired or invalid"}), 401
        
        user = User.query.get(data.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 401
        return f(user, *args, **kwargs)
    return decorated

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        serializer = URLSafeTimedSerializer(app.secret_key)
        token = serializer.dumps({"user_id": user.id})
        return jsonify({"access_token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/activity', methods=['POST'])
@require_api_token
def api_activity(user):
    data = request.get_json(silent=True) or {}
    website_name = data.get('website_name')
    st_time = data.get('st_time')
    end_time = data.get('end_time')
    
    if not (website_name and st_time and end_time):
        return jsonify({"error": "Missing payload data"}), 400
    
    try:
        duration_mins = max(1, int((end_time - st_time) / 1000 / 60))
    except (TypeError, ValueError):
        duration_mins = 1
        
    current_hour = datetime.utcnow().hour
    interval_id = current_hour // 3
    
    usage = AppUsage(
        user_id=user.id,
        app_name=website_name,
        category='Browser',
        duration_minutes=duration_mins,
        interval_id=interval_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(usage)
    db.session.commit()
    
    return jsonify({"status": "success"})


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

@app.route('/behavioral-intelligence')
@login_required
def behavioral_intelligence():
    intel_data = get_intelligence_data(current_user.id)
    return render_template('behavioral_intelligence.html', intel=intel_data, user=current_user)

@app.route('/analytics')
@login_required
def analytics_master():
    patterns = get_behavioral_patterns(current_user.id)
    trends = get_daily_trends(current_user.id)
    intel_data = get_intelligence_data(current_user.id)
    return render_template('analytics_master.html', patterns=patterns, trends=trends, intel=intel_data, user=current_user)

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
