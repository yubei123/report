from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
# from openpyxl import load_workbook
from glob import glob

app = Flask(__name__)
app.config.from_pyfile('/work/users/beitai/backend/Biotech/config.py')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(20))
    department = db.Column(db.String(64))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
        test = User(username='test', password='123', auth='实验室处理')
        test2 = User(username='test2', password='456', auth='报告分析')
        db.session.add(test)
        db.session.add(test2)
        db.session.commit()

