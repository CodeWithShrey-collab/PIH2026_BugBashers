import argparse
import random
from datetime import datetime, timedelta
from app import app
from models import db, User, AppUsage

def fill_data(username, days=7):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        
        if not user:
            print(f"Error: User '{username}' not found.")
            print("Please create the user via the web interface first.")
            return

        apps_config = [
            ("Instagram", "Social Media"),
            ("TikTok", "Social Media"),
            ("YouTube", "Entertainment"),
            ("VS Code", "Productivity"),
            ("Notion", "Productivity"),
            ("Slack", "Productivity"),
            ("Discord", "Social Media"),
            ("Netflix", "Entertainment")
        ]

        print(f"Filling {days} days of data for '{username}'...")
        
        # Determine "personality" based on existing data or random
        prob_social = random.uniform(0.2, 0.6)
        prob_prod = random.uniform(0.2, 0.6)

        start_date = datetime.utcnow() - timedelta(days=days)
        logs_created = 0
        
        for d in range(days + 1):
            current_day = start_date + timedelta(days=d)
            
            for interval in range(8):
                num_apps = random.randint(1, 3)
                for _ in range(num_apps):
                    rand = random.random()
                    if rand < prob_social:
                        app_name, cat = random.choice([a for a in apps_config if a[1] == "Social Media"])
                        dur = random.randint(30, 90)
                    elif rand < prob_social + prob_prod:
                        app_name, cat = random.choice([a for a in apps_config if a[1] == "Productivity"])
                        dur = random.randint(20, 120)
                    else:
                        app_name, cat = random.choice([a for a in apps_config if a[1] == "Entertainment"])
                        dur = random.randint(30, 120)

                    usage = AppUsage(
                        user_id=user.id,
                        app_name=app_name,
                        category=cat,
                        duration_minutes=dur,
                        timestamp=current_day.replace(hour=interval*3, minute=random.randint(0, 59)),
                        interval_id=interval
                    )
                    db.session.add(usage)
                    logs_created += 1
        
        # Update user streak/points randomly to make dashboard look active
        user.current_streak = random.randint(1, 14)
        user.total_points += random.randint(50, 500)
        
        db.session.commit()
        print(f"Successfully generated {logs_created} usage logs for {username}!")

def main():
    parser = argparse.ArgumentParser(description="Dopamine Reset - User Data Filler")
    parser.add_argument("username", help="Username of the account to fill data for")
    parser.add_argument("--days", type=int, default=7, help="Number of days of history to generate (default: 7)")
    
    args = parser.parse_args()
    
    fill_data(args.username, args.days)

if __name__ == "__main__":
    main()
