#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/20 11:43
@Author  : bellahuang
@Email   : bellahuang@webank.com
@File    : __init__.py.py
"""


from flask import Blueprint


main = Blueprint('main', __name__)
from . import views, errors
