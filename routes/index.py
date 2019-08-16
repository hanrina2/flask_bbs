import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from routes import *
from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user
from models.board import Board

import json

import redis

cache = redis.StrictRedis()


main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/signup")
def signup():
    u = current_user()
    return render_template("register.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route("/signout")
def signout():
    # u = current_user()
    # session.pop(u.id)
    session.clear()
    return redirect(url_for('.index'))


def created_topic(user_id):
    ts = Topic.all(user_id=user_id)
    return ts


def replied_topic(user_id):
    rs = Reply.all(user_id=user_id)
    ts = []
    for r in rs:
        t = Topic.one(id=r.topic_id)
        ts.append(t)
    return ts


@main.route('/image/add', methods=['POST'])
@login_required
@csrf_required
def avatar_add():
    file: FileStorage = request.files['avatar']

    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.setting'))


@main.route('/images/<filename>')
def image(filename):
    return send_from_directory('images', filename)


@main.route('/setting')
@login_required
def setting():
    board_id = int(request.args.get('board_id', -1))
    token = new_csrf_token()
    u = current_user()
    return render_template("setting.html", user=u, token=token, bid=board_id)


@main.route("/update", methods=['POST'])
@csrf_required
@login_required
def update():
    form = request.form.to_dict()
    print('form的数据', form)
    u = current_user()
    if "old_pass" in form:
        if User.salted_password(form['old_pass']) == u.password:
            form["password"] = User.salted_password(form['password'])
        else:
            return redirect(url_for('.profile'))
    User.update(u.id, **form)
    return redirect(url_for('.setting'))

