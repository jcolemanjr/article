from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    ssn = db.Column(db.String, unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    delegated_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    delegates = db.relationship('User', backref=db.backref('delegate', remote_side=[id]), lazy='dynamic')

    bills = db.relationship('Bill', backref = 'uploader', lazy=True)
    votes = db.relationship('Vote', backref = 'voter', lazy=True)


    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

class Bill(db.Model, SerializerMixin):
    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.String, unique=True, nullable=False)
    summary_id = db.Column(db.Integer, db.ForeignKey('summaries.id'), nullable=True)
    uploaded_by = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    summary = db.relationship('Summary', backref=db.backref('bill', uselist=False))
    votes = db.relationship('Vote', backref='bill', lazy=True)

class Summary(db.Model, SerializerMixin):
    __tablename__ = 'summaries'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Vote(db.Model, SerializerMixin):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bill_id = db.Column(db.Integer, db.ForeignKey('bills.id'))


