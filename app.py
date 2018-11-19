from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message


from datetime import datetime
from threading import Thread
import os


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
hostname = os.environ.get('HOSTNAME')
port = os.environ.get('PORT')
database = os.environ.get('DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(username, password, hostname, port, database)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASK_ADMIN'] = os.environ.get('FLASK_ADMIN')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX')
app.config['FLASKY_MAIL_SENDER'] = os.environ.get('FLASKY_MAIL_SENDER')
mail = Mail(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name ?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def hello_world():
    return render_template('home.html', current_time=datetime.utcnow())


@app.route('/hello/<user>')
def hello_user(user):
    return render_template('user.html', name=user)


@app.route('/sign', methods=['GET', 'POST'])
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
        return redirect(url_for('sign_up'))
    return render_template('sign_up.html', form=form, name=session.get('name'),
                           known = session.get('known', False))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error():
    return render_template('500.html'), 500


@app.route('/args')
def args_print():
    info = []
    info.append(request.form)
    info.append(request.args)
    info.append(request.values)
    info.append(request.cookies)
    info.append(request.headers)
    info.append(request.files)
    info.append(request.get_data())
    info.append(request.get_json())
    info.append(request.blueprint)
    info.append(request.endpoint)
    info.append(request.method)
    info.append(request.scheme)
    info.append(request.is_secure)
    info.append(request.host)
    info.append(request.path)
    info.append(request.query_string)
    info.append(request.full_path)
    info.append(request.url)
    info.append(request.base_url)
    info.append(request.remote_addr)
    info.append(request.environ)

    result = ''
    for i in info:
        print(i)
        result += str(i) + '\n'
    return result


if __name__ == '__main__':
    app.run()
