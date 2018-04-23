#!/usr/bin/env python
# -*- coding: utf-8
from apps import db, lm
from flask_login import UserMixin
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    token = db.Column(db.Text())
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    #密码加密
    @staticmethod
    def hash_password(self, password):
        return generate_password_hash(password)

    #密码验证
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    #获取用户
    def get(self, id):
        return self.query.filter_by(id=id).first()
    #添加用户
    # def add(self, user):
    #     if self.query.filter_by(username=user.username).first() or self.query.filter_by(email=user.email).first():
    #         return {"code": 10051,
    #                 "msg": "用户名或邮箱已存在"}
    #     db.session.add(user)
    #     db.session.commit()
    #     return {"code": 0,
    #             "msg": "添加成功"}
    @staticmethod
    def add(self, user):
        db.session.add(user)
        return session_commit()
    #更新用户
    def update(self):
        return session_commit()
    #删除用户
    @staticmethod
    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()
    # def ping(self):
    #     self.last_seen = datetime.now()
    #     db.session.add(self)
    #创建默认账户
    @staticmethod
    def create_deafult():
        admin = Users(username='admin',password='123456',email='512610309@qq.com')
        db.session.add(admin)
        db.session.commit()
    def __repr__(self):
        # rep = json.dumps({"id": self.id,
        #        "username": self.username})
        # return rep
        return '<User %r>' % self.username

class Groups(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    about = db.Column(db.Text())
    gusers = db.relationship('Users', backref='group',
                                lazy='dynamic')
    @staticmethod
    def add(group):
        db.session.add(group)
        return session_commit()
    # 更新分组
    def update(self):
        return session_commit()
    # 删除分组
    @staticmethod
    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason