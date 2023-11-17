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

@app.route('/user/<int:user_id>', methods=['GET'])
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {'username': user.username, 'firstname': user.firstname, 'lastname': user.lastname, 'email': user.email}
    return jsonify({'user': user_data})

@app.route('/user/<int:user_id>', nmethods=['PATCH'])
@token_required
def update_user_profile(current_user, user_id):
    if current_user.id != user_id:
        return jsonify({'message': 'Permission denied'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.email = data.get('email', user.email)
    user.firstname = data.get('firstname', user.firstname)
    user.middlename = data.get('middlename', user.middlename)
    user.lastname = data.get('lastname', user.lastname)
    user.suffix = data.get('suffix', user.suffix)
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    
    db.session.commit()
    return jsonify('message': 'User profile updated')

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

@app.route('/bill', methods=['GET'])
def list_bills():
    bills = Bill.query.all()
    bill_data = [{'id': bill.id, 'title': bill.title, 'summary': bill.summary, 'content': bill.content} for bill in bills]
    return jsonify({'bills': bill_data})

@app.route('/bill', methods=['POST'])
@token_required
def create_bill(current_user):
    data = request.get_json()
    new_bill = Bill(title=data['title'], content=data['content'], uploaded_by=current_user.id)
    #call OpenAI summary
    db.session.add(new_bill)
    db.session.commit()

    return jsonify({'message': 'New bill created!'})

@app.route('/bill/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    bill = Bill.query.filter_by(id=bill_id).first()

    if not bill:
        return jsonify({'message': 'No bill found!'})
    
    bill_data = {'title': bill.title, 'summary': bill.summary, 'content': bill.content, 'uploader': bill.uploader.username}
    return jsonify({'bill': bill_data})

@app.route('/bill/<int:bill_id>', methods=['PATCH'])
@token_required
def update_bill(current_user, bill_id):
    bill = Bill.query.get_or_404(bill_id)
    if bill.uploaded_by != current_user.id:
        return jsonify({'message': 'Permission denied'}), 403
    
    data = request.get_json()
    bill.title = data.get('title', bill.title)
    bill.content = data.get('content', bill.content)
    db.session.commit()
    return jsonify({'message': 'Bill updated successfully!'})

@app.route('/bill/<int:bill_id>', methods=['DELETE'])
@token_required
def delete_bill(current_user, bill_id):
    bill = Bill.query.get_or_404(bill_id)
    if bill.uploaded_by != current_user.id:
        return jsonify({'message': 'Permission denied'}), 403
    
    db.session.delete(bill)
    db.session.commit()
    return jsonify({'message': 'Bill deleted successfully'})

@app.route('/bill/<int:bill_id>/results', methods=['GET'])
def bill_results(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    votes = Vote.query.filter_by(bill_id=bill.id).all()
    results = {'Yes': 0, 'No': 0, 'Abstain': 0}
    for vote in votes:
        results[vote.vote_type] += 1
    return jsonify({'results': results})

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
