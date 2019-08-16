from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.user_role import UserRole


def reset_database():
    uri = 'mysql+pymysql://root@127.0.0.1/?charset=utf8mb4&unix_socket=/var/run/mysqld/mysqld.sock'
    # uri = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)
    e = create_engine(uri, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS flask_bbs')
        c.execute('CREATE DATABASE flask_bbs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE flask_bbs')

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='top',
        password='123',
        role = UserRole.admin
    )
    u = User.register(form)

    form = dict(
        username='top2',
        password='123123',
    )
    u = User.register(form)

    form = dict(
        title='all'
    )
    b = Board.new(form)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        board_id=b.id,
        content=content
    )

    for i in range(2):
        print('begin topic <{}>'.format(i))
        t = Topic.new(topic_form, u.id)

        reply_form = dict(
            content='reply test',
            topic_id=t.id,
        )
        for j in range(2):
            Reply.new(reply_form, u.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
