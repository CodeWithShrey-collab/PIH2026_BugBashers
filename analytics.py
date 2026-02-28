from models import AppUsage, db
from sqlalchemy import func
from datetime import datetime, timedelta

def get_behavioral_patterns(user_id):
    """
    Analyzes 3-hourly blocks to find patterns.
    """
    # 1. Category Breakdown
    category_usage = db.session.query(
        AppUsage.category, 
        func.sum(AppUsage.duration_minutes)
    ).filter(AppUsage.user_id == user_id).group_by(AppUsage.category).all()
    
    category_data = {cat: dur for cat, dur in category_usage}

    # 2. Hourly Distribution (3-hour intervals)
    interval_usage = db.session.query(
        AppUsage.interval_id,
        func.sum(AppUsage.duration_minutes)
    ).filter(AppUsage.user_id == user_id).group_by(AppUsage.interval_id).order_by(AppUsage.interval_id).all()
    
    intervals = ["00-03", "03-06", "06-09", "09-12", "12-15", "15-18", "18-21", "21-24"]
    interval_data = {intervals[i]: dur for i, dur in interval_usage}

    # 3. Dopamine Score Calculation
    # Social Media = high dopamine (multiplier 1.5)
    # Entertainment = moderate (multiplier 1.0)
    # Productivity = low (multiplier 0.2)
    social_dur = category_data.get('Social Media', 0)
    ent_dur = category_data.get('Entertainment', 0)
    prod_dur = category_data.get('Productivity', 0)
    
    total_minutes = social_dur + ent_dur + prod_dur
    if total_minutes == 0:
        dopamine_score = 0
        productivity_ratio = 0
    else:
        dopamine_score = (social_dur * 1.5 + ent_dur * 1.0 + prod_dur * 0.2) / total_minutes * 100
        productivity_ratio = int((prod_dur / total_minutes) * 100)

    # 4. Peak Distraction Window
    peak_interval = max(interval_usage, key=lambda x: x[1])[0] if interval_usage else 0
    peak_window = intervals[peak_interval]

    # 5. Most Addictive App
    top_app_record = db.session.query(
        AppUsage.app_name, func.sum(AppUsage.duration_minutes).label('total')
    ).filter(AppUsage.user_id == user_id).group_by(AppUsage.app_name).order_by(db.desc('total')).first()
    
    top_app = top_app_record[0] if top_app_record else "None"

    # 6. Context Switch Penalty (Mixing work and social in same 3h block)
    # We find how many distinct categories are used per interval per day
    # Simplified approach: If a day's interval has both Productivity and Social, it's a context switch.
    context_switch_count = 0
    raw_logs = AppUsage.query.filter_by(user_id=user_id).all()
    
    # Group by (date, interval_id) to find categories
    from collections import defaultdict
    blocks = defaultdict(set)
    for log in raw_logs:
        date_str = log.timestamp.strftime("%Y-%m-%d")
        blocks[(date_str, log.interval_id)].add(log.category)
        
    for cats in blocks.values():
        if 'Productivity' in cats and ('Social Media' in cats or 'Entertainment' in cats):
            context_switch_count += 1

    return {
        "category_data": category_data,
        "hourly_data": interval_data,
        "dopamine_score": round(dopamine_score, 1),
        "peak_window": peak_window,
        "total_time": total_minutes,
        "productivity_ratio": productivity_ratio,
        "top_app": top_app,
        "context_switches": context_switch_count
    }

def get_daily_trends(user_id, days=7):
    """
    Gets total usage per day for the last X days.
    """
    today = datetime.utcnow().date()
    trends = []
    for i in range(days):
        d = today - timedelta(days=i)
        usage = db.session.query(func.sum(AppUsage.duration_minutes)).filter(
            AppUsage.user_id == user_id,
            func.date(AppUsage.timestamp) == d
        ).scalar() or 0
        trends.append({"date": d.strftime("%Y-%m-%d"), "minutes": usage})
    
    return trends[::-1] # Return in chronological order
