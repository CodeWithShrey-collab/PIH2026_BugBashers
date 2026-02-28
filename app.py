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

WEBSITE_CATEGORIES = {
    # Social Media
    'facebook.com': 'Social Media', 'instagram.com': 'Social Media', 'twitter.com': 'Social Media', 
    'x.com': 'Social Media', 'linkedin.com': 'Social Media', 'tiktok.com': 'Social Media', 
    'snapchat.com': 'Social Media', 'reddit.com': 'Social Media', 'pinterest.com': 'Social Media', 
    'tumblr.com': 'Social Media', 'whatsapp.com': 'Social Media', 't.me': 'Social Media', 
    'telegram.org': 'Social Media', 'discord.com': 'Social Media', 'twitch.tv': 'Social Media',
    'quora.com': 'Social Media', 'wechat.com': 'Social Media', 'bereal.com': 'Social Media',
    
    # Entertainment (Video/Audio/Streaming/Gaming)
    'youtube.com': 'Entertainment', 'netflix.com': 'Entertainment', 'hulu.com': 'Entertainment', 
    'disneyplus.com': 'Entertainment', 'primevideo.com': 'Entertainment', 'spotify.com': 'Entertainment', 
    'applemusic.com': 'Entertainment', 'soundcloud.com': 'Entertainment', 'pandora.com': 'Entertainment',
    'hbo.com': 'Entertainment', 'max.com': 'Entertainment', 'paramountplus.com': 'Entertainment',
    'peacocktv.com': 'Entertainment', 'vimeo.com': 'Entertainment', 'dailymotion.com': 'Entertainment',
    'roblox.com': 'Entertainment', 'steampowered.com': 'Entertainment', 'epicgames.com': 'Entertainment',
    'ign.com': 'Entertainment', 'gamespot.com': 'Entertainment', 'crunchyroll.com': 'Entertainment',
    'imdb.com': 'Entertainment', 'rottentomatoes.com': 'Entertainment', '9gag.com': 'Entertainment',
    'buzzfeed.com': 'Entertainment',
    
    # Productivity / Work / Education
    'github.com': 'Productivity', 'gitlab.com': 'Productivity', 'bitbucket.org': 'Productivity',
    'stackoverflow.com': 'Productivity', 'notion.so': 'Productivity', 'slack.com': 'Productivity', 
    'trello.com': 'Productivity', 'asana.com': 'Productivity', 'jira.com': 'Productivity', 
    'atlassian.net': 'Productivity', 'figma.com': 'Productivity', 'canva.com': 'Productivity',
    'docs.google.com': 'Productivity', 'drive.google.com': 'Productivity', 'mail.google.com': 'Productivity',
    'calendar.google.com': 'Productivity', 'workspace.google.com': 'Productivity', 
    'office.com': 'Productivity', 'outlook.live.com': 'Productivity', 'microsoft365.com': 'Productivity',
    'zoom.us': 'Productivity', 'meet.google.com': 'Productivity', 'teams.microsoft.com': 'Productivity',
    'dropbox.com': 'Productivity', 'box.com': 'Productivity', 'chatgpt.com': 'Productivity',
    'openai.com': 'Productivity', 'claude.ai': 'Productivity', 'anthropic.com': 'Productivity',
    'perplexity.ai': 'Productivity', 'coursera.org': 'Productivity', 'udemy.com': 'Productivity',
    'edx.org': 'Productivity', 'khanacademy.org': 'Productivity', 'duolingo.com': 'Productivity',
    'codeacademy.com': 'Productivity', 'leetcode.com': 'Productivity', 'hackerrank.com': 'Productivity',
    'medium.com': 'Productivity', 'wikipedia.org': 'Productivity',
    
    # E-Commerce / Shopping
    'amazon.com': 'Shopping', 'ebay.com': 'Shopping', 'walmart.com': 'Shopping', 
    'target.com': 'Shopping', 'etsy.com': 'Shopping', 'aliexpress.com': 'Shopping',
    'alibaba.com': 'Shopping', 'shopify.com': 'Shopping', 'bestbuy.com': 'Shopping',
    'homedepot.com': 'Shopping', 'ikea.com': 'Shopping', 'shein.com': 'Shopping',
    'nike.com': 'Shopping', 'zara.com': 'Shopping', 'hm.com': 'Shopping',
    'flipkart.com': 'Shopping', 'myntra.com': 'Shopping',
    
    # News / Information
    'cnn.com': 'News', 'bbc.com': 'News', 'bbc.co.uk': 'News', 'nytimes.com': 'News', 
    'washingtonpost.com': 'News', 'theguardian.com': 'News', 'foxnews.com': 'News', 
    'wsj.com': 'News', 'bloomberg.com': 'News', 'reuters.com': 'News', 'forbes.com': 'News',
    'cnbc.com': 'News', 'nbcnews.com': 'News', 'npr.org': 'News', 'usatoday.com': 'News',
    'yahoo.com': 'News', 'msn.com': 'News', 'weather.com': 'News',

    # Browser / Search / Utils (defaults)
    'google.com': 'Browser', 'bing.com': 'Browser', 'duckduckgo.com': 'Browser',
    'yahoo.com': 'Browser', 'baidu.com': 'Browser', 'yandex.com': 'Browser'
}

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
        
    from datetime import timedelta
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    current_hour = ist_now.hour
    interval_id = current_hour // 3
    
    # Determine the category based on the domain mapping
    category = 'Browser'  # Default fallback
    if website_name:
        domain = website_name.lower().replace('www.', '')
        category = WEBSITE_CATEGORIES.get(domain, 'Browser')
    
    usage = AppUsage(
        user_id=user.id,
        app_name=website_name,
        category=category,
        duration_minutes=duration_mins,
        interval_id=interval_id,
        timestamp=ist_now
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
            
        new_user = User(username=username) # hex_code generated automatically in __init__
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

from analytics import generate_pseudo_ai_insights

@app.route('/profile')
@login_required
def profile():
    insights = generate_pseudo_ai_insights(current_user.id)
    return render_template('profile.html', user=current_user, insights=insights)

@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    if request.method == 'POST':
        hex_code = request.form.get('hex_code', '').strip().upper()
        if not hex_code:
            flash("Please enter a hex code.")
        elif hex_code == current_user.hex_code:
            flash("You cannot add yourself as a friend.")
        else:
            friend = User.query.filter_by(hex_code=hex_code).first()
            if not friend:
                flash("No user found with that hex code.")
            elif friend in current_user.friends:
                flash("You are already friends with this user.")
            else:
                current_user.friends.append(friend)
                friend.friends.append(current_user) # Mutual friendship for simplicity
                db.session.commit()
                flash(f"Successfully added {friend.username} as a friend!")
        return redirect(url_for('friends'))
    
    return render_template('friends.html', user=current_user)

from sqlalchemy import func
from models import AppUsage

@app.route('/friend/<hex_code>')
@login_required
def friend_profile(hex_code):
    # Verify the hex code belongs to a valid friend
    friend = User.query.filter_by(hex_code=hex_code).first()
    if not friend or friend not in current_user.friends:
        flash("You are not authorized to view this node's telemetry.")
        return redirect(url_for('friends'))
        
    # Calculate minimal, privacy-safe stats
    # 1. Top App
    top_app_record = db.session.query(
        AppUsage.app_name, func.sum(AppUsage.duration_minutes).label('total')
    ).filter(AppUsage.user_id == friend.id).group_by(AppUsage.app_name).order_by(db.desc('total')).first()
    
    top_app = top_app_record[0] if top_app_record else "No Data"
    
    return render_template('friend_profile.html', user=current_user, friend=friend, top_app=top_app)

import secrets
from models import Guild

@app.route('/guild', methods=['GET', 'POST'])
@login_required
def guild_dashboard():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'create':
            guild_name = request.form.get('guild_name', '').strip()
            if guild_name:
                access_code = secrets.token_hex(4).upper()
                new_guild = Guild(name=guild_name, access_code=access_code, leader_id=current_user.id)
                db.session.add(new_guild)
                db.session.flush() # get ID
                current_user.guild_id = new_guild.id
                db.session.commit()
                flash(f"Guild '{guild_name}' created successfully! Access code: {access_code}")
                
        elif action == 'join':
            access_code = request.form.get('access_code', '').strip().upper()
            guild_to_join = Guild.query.filter_by(access_code=access_code).first()
            if guild_to_join:
                current_user.guild_id = guild_to_join.id
                db.session.commit()
                flash(f"Successfully joined guild '{guild_to_join.name}'!")
            else:
                flash("Invalid access code.")
                
        elif action == 'leave':
            if current_user.guild:
                if current_user.guild.leader_id == current_user.id:
                    flash("Guild leaders cannot leave their own guild yet.")
                else:
                    current_user.guild_id = None
                    db.session.commit()
                    flash("You left the guild.")
                    
        return redirect(url_for('guild_dashboard'))
        
    guild = current_user.guild
    leaderboard = []
    guild_stats = {
        "total_points": 0,
        "total_productivity_hours": 0,
        "top_distraction": "N/A"
    }
    
    if guild:
        # Sort members by points descending
        leaderboard = sorted(guild.members, key=lambda x: x.total_points, reverse=True)
        
        # Calculate Aggregated Stats
        member_ids = [m.id for m in guild.members]
        if member_ids:
            # Total Productivity Time (in hours)
            prod_mins = db.session.query(func.sum(AppUsage.duration_minutes)).filter(
                AppUsage.user_id.in_(member_ids),
                AppUsage.category == 'Productivity'
            ).scalar() or 0
            guild_stats["total_productivity_hours"] = round(prod_mins / 60, 1)
            
            # Top Distracting App (Social/Entertainment)
            top_dist_record = db.session.query(
                AppUsage.app_name, func.sum(AppUsage.duration_minutes).label('total')
            ).filter(
                AppUsage.user_id.in_(member_ids),
                AppUsage.category.in_(['Social Media', 'Entertainment'])
            ).group_by(AppUsage.app_name).order_by(db.desc('total')).first()
            
            guild_stats["top_distraction"] = top_dist_record[0] if top_dist_record else "None"
            
            guild_stats["total_points"] = sum(m.total_points for m in guild.members)
        
    return render_template('guild.html', user=current_user, guild=guild, leaderboard=leaderboard, guild_stats=guild_stats)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a default user if none exists
        if not User.query.first():
            default_user = User(username="default_user")
            default_user.set_password("password") # Provide a default password
            db.session.add(default_user)
            db.session.commit()
            print("Default user created.")
    
    app.run(debug=True, port=5000)
