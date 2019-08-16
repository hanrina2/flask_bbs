import time

from flask import Flask
from routes import current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import secret
import config
from models.base_model import db
from models.user import User
from models.user_role import UserRole
from models.board import Board
from utils import log
from datetime import timedelta

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.profile import main as profile_routes
from routes.message import main as mail_routes, mail


class UserModelView(ModelView):
    column_searchable_list = ('username', 'password')

    def is_accessible(self):
        u = current_user()
        return u.role == UserRole.admin


class BoardModelView(ModelView):
    column_searchable_list = ['title']

    def is_accessible(self):
        u = current_user()
        return u.role == UserRole.admin


def count(input):
    log('jinja2过滤 ，计数')
    return len(input)


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted


def configured_app():
    app = Flask(__name__)
    app.secret_key = secret.secret_key

    uri = 'mysql+pymysql://root@127.0.0.1/flask_bbs?charset=utf8mb4&unix_socket=/var/run/mysqld/mysqld.sock'

    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/flask_bbs?charset=utf8mb4'.format(
    #    secret.database_password
    #)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    '''
    app.config['MAIL_SERVER'] = 'smtp.exmail.qq.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = config.admin_mail
    app.config['MAIL_PASSWORD'] = secret.mail_password

    mail.init_app(app)
    '''
    admin = Admin(app, name='bbs admin', template_mode='bootstrap3')
    u = UserModelView(User, db.session)
    u.column_searchable_list = ["username", "password"]
    admin.add_view(u)
    b = BoardModelView(Board, db.session)
    b.column_searchable_list = ["title"]
    admin.add_view(b)
    app.permanent_session_lifetime = timedelta(minutes=60)
    register_routes(app)
    return app


def register_routes(app):

    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(profile_routes, url_prefix='/user')

    app.template_filter()(count)
    app.template_filter()(format_time)


if __name__ == '__main__':
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
