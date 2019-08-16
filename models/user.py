import hashlib

from sqlalchemy import Column, String, UnicodeText, Enum


import config
import secret
from models.base_model import SQLMixin, db
from models.user_role import UserRole


class User(SQLMixin, db.Model):
    __tablename__ = 'User'
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    signature = Column(UnicodeText, nullable=False, default='个性签名')
    role = Column(Enum(UserRole), nullable=False, default=UserRole.normal)
    image = Column(String(100), nullable=False, default='/images/3.jpg')
    email = Column(String(50), nullable=False, default=config.test_mail)

    @staticmethod
    def guest():
        u = User()
        u.username = '【游客】'
        u.password = '【游客】'
        u.role = UserRole.guest
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)


