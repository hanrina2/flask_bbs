from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board
from models.reply import Reply

main = Blueprint('topic', __name__)


@main.route("/")
@login_required
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    user = User.one(id=u.id)
    return render_template("topic/index.html", ms=ms, token=token, bs=bs, bid=board_id, user=user)


@main.route('/<int:id>')
@login_required
def detail(id):
    u = current_user()
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m, user=u)


@main.route("/delete")
@login_required
@topic_owner_required
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    m = Reply.all(topic_id=id)
    for i in m:
        Reply.delete(i.id)
    return redirect(url_for('.index'))


@main.route("/new")
@login_required
def new():
    u = current_user()
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id, user=u)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    print('form是', form)
    Topic.new(form, user_id=u.id)
    return redirect(url_for('.index'))
