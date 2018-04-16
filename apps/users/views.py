#!/usr/bin/env python
# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource, abort

from apps.users.models import Users
import apps.common as common
from apps.auth.auths import Auth
def abort404():
    abort(404, message=u"造访月球中!")
class Hello(Resource):
    def get(self):
        msg = {'data': 'This is AUTH GET!'}
        return jsonify(msg)

    def post(self):
        msg = {'data': 'This is AUTH POST!'}
        return jsonify(msg)

#检查提交用户信息是否冲突
def check_users(username,email):
    if Users.query.filter_by(username=username).first() is None and Users.query.filter_by(email=email).first() is None:
        return 0    #用户名与邮箱都可用
    elif Users.query.filter_by(username=username).first() is not None and Users.query.filter_by(email=email).first() is None:
        return 1    #用户名不可用,邮箱可用
    elif Users.query.filter_by(username=username).first() is None and Users.query.filter_by(email=email).first() is not None:
        return 2    #用户名可用,邮箱不可用
    elif Users.query.filter_by(username=username).first() is not None and Users.query.filter_by(email=email).first() is not None:
        return 3    #用户名邮箱都不可用
#用户注册
class Register(Resource):
    def get(self):
        pass
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        name = request.json.get('name')
        email = request.json.get('email')
        about_me = request.json.get('about_me')
        if check_users(username,email) == 1:
            return jsonify(common.falseReturn("用户名已被占用", "用户注册失败"))
        elif check_users(username,email) == 2:
            return jsonify(common.falseReturn("该邮箱已经注册过", "用户注册失败"))
        elif check_users(username,email) == 3:
            return jsonify(common.falseReturn("用户名邮箱都不可用", "用户注册失败"))

        user = Users(username=username,
                     password=Users.hash_password(Users, password),
                     name=name,
                     email=email,
                     about_me=about_me,)
        res = Users.add(Users, user)
        if user.id:
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return jsonify(common.trueReturn(returnUser, "用户注册成功"))
        else:
            return jsonify(common.falseReturn(res, '用户注册失败'))
#用户列表
class UserList(Resource):
    def get(self):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            try:
                u_list = []
                for u in Users.query.all():
                    u_list.append({"id": u.id,
                                   "username": u.username,
                                   "name": u.name,
                                   "email": u.email,
                                   "isAdmin": u.isAdmin,
                                   "member_since": str(u.member_since),
                                   "about_me": u.about_me,
                                   })
                result = common.trueReturn(u_list, u"请求成功")
            except Exception as e:
                result = common.falseReturn(e, "请求失败")
        else:
            result = common.falseReturn(iauth['data'], "请求失败")
        return result
#用户更新
class UpdUser(Resource):
    def post(self):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            try:
                user = Users.query.filter_by(username=request.json.get('username')).first()
                user.password = Users.hash_password(Users, request.json.get('password'))
                user.name = request.json.get('name')
                user.email = request.json.get('email')
                user.about_me = request.json.get('about_me')
                a = user.update()
                result = common.trueReturn('用户更新成功', "请求成功")
            except Exception as e:
                result = common.falseReturn(e, "请求失败")
        else:
            result = common.falseReturn(iauth['data'], "请求失败")
        return jsonify(result)
#用户删除
class DelUser(Resource):
    def get(self,userid):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            if userid == iauth['data']['id']:
                return common.falseReturn('不能删除自己.', "请求失败")

            if iauth['data']['isAdmin']:
                try:
                    Users.delete(Users, userid)
                    result = common.trueReturn('用户删除成功.', "请求成功")
                except Exception as e:
                    result = common.falseReturn(e, "请求失败")
            else:
                result = common.falseReturn('权限不足.', "请求失败")
        else:
            result = common.falseReturn(iauth['data'], "请求失败")
        return result
class get_info(Resource):
    def get(self):
        result = Auth.identify(Auth, request)
        if result['status']:
            result = common.trueReturn(result['data'], "请求成功")
        else:
            result = common.falseReturn(result['data'], "请求失败")
        return jsonify(result)
