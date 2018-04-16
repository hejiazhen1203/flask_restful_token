#coding: utf-8
from app import db
from ..models import User,Role
from werkzeug.security import generate_password_hash
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def exist_user(username):
    return User.query.filter_by(username=username).first() is not None

def add_user(username,password,name=None,role=None,email=None,about=None):
    if exist_user(username):
        return {"status":1,
                "msg":"用户已存在"}
    else:
        try:
            if role == 'su':
                role = Role.query.filter_by(name='Administrator').first()
            elif role == 'cu':
                role = Role.query.filter_by(name='User').first()
            print role
            user = User(username=username, password=password, role=role, name=name,email=email,about_me=about)
            db.session.add(user)
            db.session.commit()
            return {"status": 0,
                    "msg": "添加成功"}
        except Exception as e:
            print  e
            return {"status": 2,
                    "msg": "数据库错误"}
def del_user(userid):
    try:
        user = User.query.filter_by(id=userid).first()
        db.session.delete(user)
        db.session.commit()
        return {"status": 0,
                "msg": "删除成功"}
    except:
        return {"status": 1,
                "msg": "删除失败"}
def upd_user(username,password,nickname,email):
    try:
        user = User.query.filter_by(username=username).first()
        if user.password != password:
            user.password = generate_password_hash(password)
        user.nick_name = nickname
        user.email = email
        db.session.commit()
        return {"status": 0,
                "msg": "更新成功"}
    except:
        return {"status": 1,
                "msg": "更新失败"}