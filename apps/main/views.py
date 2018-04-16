#!/usr/bin/env python
# -*- coding: utf-8

from flask import jsonify, request
from flask_restful import Resource, abort
from apps.auth.auths import Auth
import apps.common as common
from apps.users.models import Users
from datetime import datetime
def abort404():
    abort(404, message=u"造访月球中!")
class Hello(Resource):
    def get(self):
        msg = {'data': 'This is main GET!'}
        return jsonify(msg)

    def post(self):
        msg = {'data': 'This is main POST!'}
        abort404()
        return jsonify(msg)

#用户登录
class Login(Resource):
    def get(self):
        pass
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = Users.query.filter_by(username=username).first()
        if user:
            if user.verify_password(password):
                user.last_seen = datetime.now()
                a = user.update()
                # print a
                # return jsonify(common.trueReturn('', "用户登录成功"))
                token =  Auth.authenticate(Auth, user)
                return jsonify(common.trueReturn(token, "用户登录成功"))
            else:
                return jsonify(common.falseReturn('', '用户或密码错误'))
        else:
            return jsonify(common.falseReturn('', '用户不存在'))