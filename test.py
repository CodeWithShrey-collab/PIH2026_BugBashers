import json
from app import app
from models import User

def check_dashboard():
    with app.test_client() as tc:
        with app.app_context():
            user = User.query.filter_by(username='h').first()
            if not user:
                print("No user h")
                return
            
            with tc.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True
        
        resp = tc.get('/analytics')
        print(resp.status_code)
        
if __name__ == '__main__':
    check_dashboard()
