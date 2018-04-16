#!/usr/bin/env python
# -*- coding: utf-8
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()   #数据模型
lm = LoginManager()     #登录模块
def create_app(config_name):
    app = Flask(__name__, static_folder='', static_url_path='')
    app.config.from_object(config[config_name])
    CORS(app, supports_credentials=True)    #解决跨域

    db.init_app(app)
    lm.init_app(app)

    #路由
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')
    return app
