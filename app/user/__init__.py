
from flask import Blueprint, request
from app.models import User, route_auth, logger, Log
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

user = Blueprint('user', __name__)

##获取token,用于后续的jwt验证
@user.post('/get_auth')
def get_auth():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if not user:
        return {'msg': f'用户不存在！', 'code': 400}
    if password != user.password:
        return {'msg': f'用户密码错误！', 'code': 400}
    return {'msg': '已获取Token！', 'code': 200, 'token': user.generate_auth_token()}

##验证token是否有效并登录
@user.post('/login')
@jwt_required()
def login():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    auth = user.auth
    return {'auth':auth, 'msg':'已登录！', 'code':200}

##注册新用户
@user.post('/addUser')
def addUser():
    username = request.json['username']
    password = request.json['password']
    auth = request.json['auth']
    user = User.query.filter_by(username=username).first()
    if user:
        return {'msg':'用户已存在！', 'code':400}
    else:
        u = User(username=username, password=password, auth=auth)
        db.session.add(u)
        db.session.commit()
        return {'msg':'注册成功！', 'code':200}

##修改用户密码
@user.post('/changePassword')
@jwt_required()
def changePassword():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user:
        user.update(**{'password':password})
        db.session.commit()
        return {'msg':'密码修改成功！', 'code':200}
    else:
        return {'msg':'用户不存在！', 'code':400}
