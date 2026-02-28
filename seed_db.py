import random
from datetime import datetime, timedelta
from app import app
from models import db, User, AppUsage

def seed_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        users_info = [
            {"username": "JohnDoe", "streak": 5, "points": 450},
            {"username": "JaneSmith", "streak": 12, "points": 1200},
            {"username": "AlexPro", "streak": 2, "points": 150}
        ]

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

        for u_info in users_info:
            user = User(
                username=u_info["username"],
                current_streak=u_info["streak"],
                total_points=u_info["points"]
            )
            # Default password for all seeded users is 'password'
            user.set_password('password')
            db.session.add(user)
            db.session.flush() # Get user.id

            # Generate data for the last 7 days
            start_date = datetime.utcnow() - timedelta(days=7)
            
            for d in range(8):
                current_day = start_date + timedelta(days=d)
                
                # Each user has a "personality"
                if user.username == "JaneSmith": # High productivity
                    prob_social = 0.1
                    prob_prod = 0.7
                elif user.username == "JohnDoe": # Balanced
                    prob_social = 0.4
                    prob_prod = 0.4
                else: # AlexPro - High distraction
                    prob_social = 0.7
                    prob_prod = 0.1

                for interval in range(8):
                    # Randomly pick apps based on personality
                    num_apps = random.randint(1, 3)
                    for _ in range(num_apps):
                        rand = random.random()
                        if rand < prob_social:
                            app_name, cat = random.choice([a for a in apps_config if a[1] == "Social Media"])
                            dur = random.randint(30, 60)
                        elif rand < prob_social + prob_prod:
                            app_name, cat = random.choice([a for a in apps_config if a[1] == "Productivity"])
                            dur = random.randint(20, 90)
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
        
        db.session.commit()
        print("Database seeded with multiple users and varied patterns.")

if __name__ == "__main__":
    seed_data()
