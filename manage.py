#!/usr/bin/env python
# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from run import myapp
from apps import db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand



manager = Manager(myapp)
migrate = Migrate(myapp, db)
manager.add_command('db', MigrateCommand)

# @manager.command
# def deploy():
#     """Run deployment tasks."""
#     from flask_migrate import upgrade
#     from app.models import Role, User
#
#     # migrate database to latest revision
#     upgrade()
#
#     # create user roles
#     Role.insert_roles()
#     User.create_deafult()


if __name__ == '__main__':
    manager.run()
