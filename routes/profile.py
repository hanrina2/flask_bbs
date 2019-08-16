from flask import (
    render_template,
    Blueprint,
)

from routes import *
from routes import current_user
from routes.index import created_topic
from models.reply import Reply
from models.user import User


main = Blueprint('profile', __name__)


@main.route('/<username>')
@login_required
def profile(username):
    user = current_user()
    u = User.one(username=username)
    if u == user:
        t = created_topic(u.id)
        topics = [i for i in reversed(t)]
        r = Reply.all(user_id=u.id)
        for i in r:
            print('测试', i.topic())
        replys = [i for i in reversed(r)]
        return render_template("user_profile.html", topics=topics, replys=replys, user=u)
    else:
        return redirect(url_for('topic.index'))