import uuid
from functools import wraps

from flask import session, request, abort, redirect, url_for

from models.user import User
from models.topic import Topic

import json
import redis

cache = redis.StrictRedis()


def current_user():
    if 'user_id' in session:
        user_id = int(session['user_id'])
        u = User.one(id=user_id)
        return u
    else:
        return User.guest()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        print('字典', cache)
        if cache.exists(token) and json.loads(cache.get(token)) == u.id:
            cache.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    cache.set(token, u.id)
    return token


def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        print('login_required')
        u = current_user()
        if u.is_guest():
            print('游客用户')
            return redirect(url_for('index.index'))
        else:
            print('登录用户', f)
            return f(*args, **kwargs)

    return wrapper


def topic_owner_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        print('login_required')
        u = current_user()
        if 'id' in request.args:
            topic_id = request.args['id']
        else:
            topic_id = request.form['id']
        t = Topic.one(id=int(topic_id))

        if t.user_id == u.id:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('topic.index'))

    return wrapper
