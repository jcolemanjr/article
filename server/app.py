from flask import request, make_response, session, jsonify, abort
from werkzeug.exceptions import HTTPException
from config import app, db
from models import User, UserMedia, Media
import requests

from flask import Flask, request, jsonify, make_response
from models import db, User, Bill, Summary, Vote
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import app, db
import jwt
import datetime
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route('/delegate', methods=['POST'])
@token_required
def delegate_vote(current_user):
    data = request.get_json()
    user_to_delegate_to = User.query.filter_by(username=data['delegate_to']).first()

    if not user_to_delegate_to:
        return jsonify({'message': 'User to delegate to not found!'}), 404
    
    if user_to_delegate_to.id == current_user.id or user_to_delegate_to.delegated_to == current_user.id:
        return jsonify({'message': 'Invalid delegation request!'}), 400
    
    current_user.delegated_to = user_to_delegate_to.id
    db.session.commit()

    return jsonify({'message': f'You have delegated your vote to {user_to_delegate_to.username}.'})


@app.route('/revoke_delegate', methods=['POST'])
@token_required
def revoke_delegate(current_user):
    current_user.delegated_to = None
    db.session.commit()

    return jsonify({'message': 'You have revoked your vote delegation.'})

@app.route('/vote', methods=['POST'])
@token_required
def vote_on_bill(current_user):
    data = request.get_json()
    bill_id = data['bill_id']
    vote_type = data['vote_type']

    final_delegate = current_user

    while final_delegate.delegated_to:
        final_delegate = User.query.get(final_delegate.delegated_to)

    new_vote = Vote(user_id=final_delegate.id, bill_id=bill_id, vote_type=vote_type)

    db.session.add()
    db.session.commit()

    return jsonify({'message': 'Vote cast!'})


if __name__ == '__main__':
    app.run(debug=True)
