from models import db, User, Bill, Summary, Vote
from werkzeug.security import generate_password_hash
from datetime import datetime

def delete_data():
    db.session.query(Vote).delete()
    db.session.query(Summary).delete()
    db.session.query(Bill).delete()
    db.session.query(User).delete()
    db.session.commit()

def create_users():
    users = [
        User(username="user1", password=generate_password_hash("password1"), email="user1@example.com"),
        User(username="user2", password=generate_password_hash("password2"), email="user2@example.com"),
        # Add more users as needed
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()

def create_bills():
    bills = [
        Bill(title="Bill 1", content="Content for Bill 1", uploaded_by=1),
        Bill(title="Bill 2", content="Content for Bill 2", uploaded_by=2),
        # Add more bills as needed
    ]
    db.session.bulk_save_objects(bills)
    db.session.commit()

def create_summaries():
    summaries = [
        Summary(content="Summary for Bill 1", bill_id=1),
        Summary(content="Summary for Bill 2", bill_id=2),
        # Add more summaries as needed
    ]
    db.session.bulk_save_objects(summaries)
    db.session.commit()

def create_votes():
    votes = [
        Vote(user_id=1, bill_id=1, vote_type="Yes"),
        Vote(user_id=2, bill_id=1, vote_type="No"),
        # Add more votes as needed
    ]
    db.session.bulk_save_objects(votes)
    db.session.commit()

def seed_database():
    delete_data()
    create_users()
    create_bills()
    create_summaries()
    create_votes()
    print("Database seeded!")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed_database()
