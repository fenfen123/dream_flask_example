#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/20 11:58
@Author  : bellahuang
@Email   : bellahuang@webank.com
@File    : flasky.py
"""


from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


if __name__ == '__main__':
    app.run()