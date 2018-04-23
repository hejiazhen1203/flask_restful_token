#!/usr/bin/env python
# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from datetime import datetime
from flask import jsonify, request
from flask_restful import Resource, abort

from apps.users.models import Users, Groups
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

# 检查分组是否冲突
def check_group(name):
    if Groups.query.filter_by(name=name).first() is None:
        return True  # 分组名可用

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
            resp = {
                "code": 10021,
                "status": False,
                "msg": "该用户名已被使用",
                "data": ""
            }
            return jsonify(resp)
            # return jsonify(common.falseReturn("用户名已被占用", "用户注册失败"))
        elif check_users(username,email) == 2:
            resp = {
                "code": 10022,
                "status": False,
                "msg": "该邮箱已经注册过",
                "data": ""
            }
            return jsonify(resp)
        elif check_users(username,email) == 3:
            resp = {
                "code": 10023,
                "status": False,
                "msg": "用户名邮箱都不可用",
                "data": ""
            }
            return jsonify(resp)
        user = Users(username=username,
                     password=Users.hash_password(Users, password),
                     name=name,
                     email=email,
                     about_me=about_me,)
        res = Users.add(Users, user)
        if user.id:
            resp = {
                "code": 0,
                "status": True,
                "msg": "注册成功",
                "data": {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }
            return jsonify(resp)
        else:
            resp = {
                "code": 10020,
                "status": False,
                "msg": "用户注册失败",
                "data": res
            }
            return jsonify(resp)
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
                resp = {
                    "code": 0,
                    "status": True,
                    "msg": "用户列表获取成功",
                    "data": u_list
                }
            except Exception as e:
                resp = {
                    "code": 10031,
                    "status": False,
                    "msg": "用户列表获取失败",
                    "data": e
                }
        else:
            resp = {
                "code": 10032,
                "status": False,
                "msg": "用户列表获取失败",
                "data": iauth['data']
            }
        return jsonify(resp)
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
                resp = {
                    "code": 0,
                    "status": True,
                    "msg": "用户资料更新成功",
                    "data": ""
                }
            except Exception as e:
                resp = {
                    "code": 10041,
                    "status": False,
                    "msg": "用户资料更新失败",
                    "data": e
                }
        else:
            resp = {
                "code": 10042,
                "status": False,
                "msg": "用户资料更新失败",
                "data": iauth['data']
            }
        return jsonify(resp)
#用户删除
class DelUser(Resource):
    def get(self,userid):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            if userid == iauth['data']['id']:
                resp = {
                    "code": 10051,
                    "status": False,
                    "msg": "用户删除失败",
                    "data": "不能删除自己"
                }

            if iauth['data']['isAdmin']:
                try:
                    Users.delete(Users, userid)
                    resp = {
                        "code": 0,
                        "status": True,
                        "msg": "用户删除成功",
                        "data": ""
                    }
                except Exception as e:
                    resp = {
                        "code": 10052,
                        "status": False,
                        "msg": "用户删除失败",
                        "data": e
                    }
            else:
                resp = {
                    "code": 10053,
                    "status": False,
                    "msg": "用户删除失败",
                    "data": "权限不足"
                }
        else:
            resp = {
                "code": 10053,
                "status": False,
                "msg": "用户删除失败",
                "data": iauth['data']
            }
        return jsonify(resp)
#创建分组
class CreatGroup(Resource):
    def post(self):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            if iauth['data']['isAdmin']:
                name = request.json.get('groupname')
                about = request.json.get('about')
                if check_group(name):
                    group = Groups(name=name, about=about)
                    res = Groups.add(group)
                    if group.id:
                        result = common.trueReturn({'id': group.id, 'name': group.name}, "请求成功")
                    else:
                        result = common.falseReturn(res, '请求失败')
                else:
                    result = common.falseReturn('该分组已存在', '请求失败')
            else:
                result = common.falseReturn('权限不足.', "请求失败")

        else:
            result = common.falseReturn(iauth['data'], "请求失败")
        return jsonify(result)
#删除分组
class DelGroup(Resource):
    def get(self, groupid):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            if iauth['data']['isAdmin']:
                try:
                    Groups.delete(Groups, groupid)
                    result = common.trueReturn('删除分组成功.', "请求成功")
                except Exception as e:
                    result = common.falseReturn(e, "请求失败")
            else:
                result = common.falseReturn('权限不足.', "请求失败")
        else:
            result = common.falseReturn(iauth['data'], "请求失败")
        return result
#更新分组
class UpdGroup(Resource):
    def post(self):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            try:
                group = Groups.query.filter_by(id=request.json.get('id')).first()
                if not check_group(request.json.get('groupname')):
                    result = common.falseReturn('该分组名字已存在', "请求失败")
                else:
                    group.name = request.json.get('groupname')
                    group.about = request.json.get('about')
                    a = group.update()
                    result = common.trueReturn('分组更新成功', "请求成功")
            except Exception as e:
                result = common.falseReturn(e, "请求失败")
        else:
            result = common.falseReturn(iauth['data'], "请求失败")
        return jsonify(result)
#分组列表
class GroupList(Resource):
    def get(self):
        iauth = Auth.identify(Auth, request)
        if iauth['status']:
            try:
                g_list = []
                for g in Groups.query.all():
                    g_list.append({"id": g.id,
                                   "name": g.name,
                                   "about": g.about,
                                   })
                result = common.trueReturn(g_list, u"请求成功")
            except Exception as e:
                result = common.falseReturn(e, "请求失败")
        else:
            result = common.falseReturn(iauth['data'], "请求失败")
        return result

class get_info(Resource):
    def get(self):
        result = Auth.identify(Auth, request)
        if result['status']:
            user = Users.query.filter_by(username=result["data"]["username"]).first()
            print user.group.gusers.all()
            # Groups.delete(Groups, 1)
        else:
            result = common.falseReturn(result['data'], "请求失败")
        return jsonify(result)
