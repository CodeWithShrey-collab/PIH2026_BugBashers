from app import app, db

def reset_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database dropped and recreated successfully with the new schema.")

if __name__ == '__main__':
    reset_database()
