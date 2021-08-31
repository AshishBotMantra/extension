from extension import db,app
from flask import jsonify,request,make_response
from ..users.models import User
from ..users.schema import users_schema,user_schema
from ..users import user
import uuid
from datetime import datetime,timedelta,timezone
import jwt
from werkzeug.security import check_password_hash,generate_password_hash
from extension.authorization.auth import token_required
from . import schema

app.config['SECRET_KEY'] = 'thesecretkey'

@user.route('/user',methods=['GET'])
@token_required
def get_all_user(current_user):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    all_user = User.query.all()
    result = users_schema.dump(all_user)
    return jsonify(result)

@user.route('/user/<public_id>',methods=['GET'])
@token_required
def get_user(current_user,public_id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    single_user = User.query.filter_by(public_id=public_id).first()

    return user_schema.jsonify(single_user)

@user.route('/user',methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    name = request.json['name']
    password = request.json['password']
    if User.query.filter_by(name = name).first():
        return jsonify({"message":"name is already used"})
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(public_id=str(uuid.uuid4()),name=name,password=hashed_password,admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"new user created"})

@user.route('user/<public_id>',methods=['PUT'])
@token_required
def promote_user(current_user,public_id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    single_user = User.query.filter_by(public_id=public_id).first()

    single_user.admin = True
    db.session.commit()
    return jsonify({"message":"user has beem promoted"})

@user.route('user/<public_id>',methods=['DELETE'])
@token_required
def delete_user(current_user,public_id):
    if not current_user.admin:
        return jsonify({"message":"cannot perform that function"})
    single_user = User.query.filter_by(public_id=public_id).first()
    db.session.delete(single_user)
    db.session.commit()
    return jsonify({"message":"user has been deleted"})


@app.route('/login')

def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify',403,{'www-authenticate' : 'Basic-realm="Login required'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('could not verify', 403, {'www-authenticate': 'Basic-realm="Login required'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id':user.public_id, 'exp': datetime.now(timezone.utc) + timedelta(minutes=10)},
                           app.config['SECRET_KEY'])
        return jsonify({"token": token})
    return make_response('could not verify', 403, {'www-authenticate': 'Basic-realm="Login required'})

