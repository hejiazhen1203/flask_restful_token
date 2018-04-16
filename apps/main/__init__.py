#!/usr/bin/env python
# -*- coding: utf-8
from flask import Blueprint
from flask_restful import Api
from . import views
# main = Blueprint('main', __name__, template_folder='pages')
main = Blueprint('main', __name__)
api = Api(main)
api.add_resource(views.Hello, '/')
api.add_resource(views.Login, '/login')
