#!/usr/bin/env python
# -*- coding: utf-8

from flask import Blueprint
from flask_restful import Api

from . import views
users = Blueprint('users', __name__)
api = Api(users)
api.add_resource(views.Hello, '/')
api.add_resource(views.Register, '/register')
api.add_resource(views.DelUser, '/deluser/<int:userid>')
api.add_resource(views.UserList, '/list')
api.add_resource(views.UpdUser, '/update')
api.add_resource(views.CreatGroup, '/addgroup')
api.add_resource(views.DelGroup, '/delgroup/<int:groupid>')
api.add_resource(views.UpdGroup, '/updgroup')
api.add_resource(views.GroupList, '/listgroup')

api.add_resource(views.get_info, '/info')
