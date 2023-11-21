from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from config import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=True)
    firstname = db.Column(db.String, nullable=True)
    middlename = db.Column(db.String, nullable=True)
    lastname = db.Column(db.String, nullable=True)
    suffix = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)
    ssn = db.Column(db.String, unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    delegated_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    delegates = db.relationship('User', backref=db.backref('delegate', remote_side=[id]), lazy='dynamic')

    bills = db.relationship('Bill', backref = 'uploader', lazy=True)
    votes = db.relationship('Vote', backref = 'voter', lazy=True)

    serialize_rules = ('-delegates.user', '-delegates.delegate') #Check these


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def delegate_vote(self, user_id):
        self.delegated_to = user_id
        pass

    def revoke_delegation(self):
        self.delegated_to = None
        pass

    def cast_vote(self):
        pass
    

class Bill(db.Model, SerializerMixin):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.String, unique=True, nullable=False)
    # summary_id = db.Column(db.Integer, db.ForeignKey('summaries.id'), nullable=True)
    uploaded_by = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    summary = db.relationship('Summary', backref=db.backref('bill', uselist=False))
    votes = db.relationship('Vote', backref='bill', lazy=True)

    serialize_rules = ('-votes.bill', '-summary.bill')

    def generate_summary(self):
        #GPT logic
        pass

    def vote_count(self):
        votes = Vote.query.filter_by(bill_id=self.id).all()
        return{'Yes': len([vote for vote in votes if vote.vote_type == 'Yes']),
               'No': len([vote for vote in votes if vote.vote_type == 'No']),
               'Abstain': len([vote for vote in votes if vote.vote_type == 'Abstain'])}

class Summary(db.Model, SerializerMixin):
    __tablename__ = 'summaries'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'), nullable=True)
    # bill = db.relationship('Bill', backref='summary', lazy=True)

    def formatted_summary(self):
        #summary logic
        return self.summary


class Vote(db.Model, SerializerMixin):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'))
    vote_type = db.Column(db.String, nullable=False)

    def vote_dict(self):
        return {'user_id': self.user_id, 'bill_id': self.bill_id, 'vote_type': self.vote_type}


