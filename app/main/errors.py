#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/20 11:43
@Author  : bellahuang
@Email   : bellahuang@webank.com
@File    : errors.py
"""


from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_error():
    return render_template('500.html'), 500