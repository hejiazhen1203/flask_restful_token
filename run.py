#!/usr/bin/env python
# -*- coding: utf-8
from apps import create_app

myapp = create_app('default')

if __name__ == '__main__':
    myapp.run(host='0.0.0.0', debug = True)