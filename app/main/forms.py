#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/20 11:44
@Author  : bellahuang
@Email   : bellahuang@webank.com
@File    : forms.py
"""


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name ?', validators=[DataRequired()])
    submit = SubmitField('Submit')