#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2018/11/20 11:44
@Author  : bellahuang
@Email   : bellahuang@webank.com
@File    : views.py
"""


from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from ..models import User
from ..email import send_email
from .. import db
from .. import create_app


app = create_app('default')


@main.route('/')
def hello_world():
    return render_template('home.html', current_time=datetime.utcnow())


@main.route('/hello/<user>')
def hello_user(user):
    return render_template('user.html', name=user)


@main.route('/sign', methods=['GET', 'POST'])
def sign_up():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        print(user)
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASK_ADMIN']:
                send_email(app.config['FLASK_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        # session['name'] = form.name.data
        # old_name = session.get('name')
        # if old_name is not None and old_name != form.name.data:
        #     flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # 防止post作为最后一个请求
        return redirect(url_for('.sign_up'))
    return render_template('sign_up.html', form=form, name=session.get('name'),
                           known = session.get('known', False))