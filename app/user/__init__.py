
from flask import Blueprint, request
from app.models import User, route_auth, logger, Log
from app import db
from flask_jwt_extended import jwt_required

user = Blueprint('user', __name__)

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
    