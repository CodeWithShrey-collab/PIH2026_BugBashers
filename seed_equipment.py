from app import app, db
from models import Equipment

def seed_db():
    with app.app_context():
        # Clear existing just in case
        Equipment.query.delete()
        db.session.commit()
        
        items = [
            Equipment(name='Rusty Spoon of Discipline', type='Weapon', effect_type='attack', effect_value=5, cost=30),
            Equipment(name='Sword of Focus', type='Weapon', effect_type='attack', effect_value=15, cost=100),
            Equipment(name='Aegis of Willpower', type='Armor', effect_type='defense', effect_value=10, cost=85),
            Equipment(name='Cloak of Serenity', type='Armor', effect_type='defense', effect_value=25, cost=180),
            Equipment(name='Frozen Hourglass', type='Artifact', effect_type='regen_freeze', effect_value=1, cost=500),
            Equipment(name='Scroll of Wisdom', type='Artifact', effect_type='xp_boost', effect_value=1.5, cost=300)
        ]
        
        for item in items:
            db.session.add(item)
            
        db.session.commit()
        print("Equipment armory has been fully seeded with early and mid-game items.")

if __name__ == '__main__':
    seed_db()
