#!/usr/bin/env python
# -*- coding: utf-8
from apps import db, lm
from flask_login import UserMixin
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class test1(UserMixin, db.Model):
    __tablename__ = 'test1'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128))
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, **kwargs):
        super(test1, self).__init__(**kwargs)

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
    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()
    # def ping(self):
    #     self.last_seen = datetime.now()
    #     db.session.add(self)
    #创建默认账户
    @staticmethod
    def create_deafult():
        admin = test1(username='admin',password='123456',email='512610309@qq.com')
        db.session.add(admin)
        db.session.commit()
    def __repr__(self):
        return '<User %r>' % self.username

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason