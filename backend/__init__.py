# coding: utf8

from emmett import App
from emmett.orm import Database
from emmett.tools.auth import Auth
# from emmett.tools import Mailer
from emmett.sessions import SessionManager

from .models.users import User
from .models.posts import Post
from .models.subscriptions import Subscription
from emmett_rest import REST

app = App(__name__)
app.use_extension(REST)
app.config.REST.default_pagesize = 200
app.config.REST.min_pagesize = 10
app.config.REST.max_pagesize = 5000

# Config
# app.config_from_yaml('app.yml')
# app.config_from_yaml('db.yml', 'db')
# app.config_from_yaml('mailer.yml', 'mailer')
# app.config_from_yaml('auth.yml', 'auth')
app.config.db.uri = 'sqlite://database.sqlite'

db = Database(app, auto_migrate=False)
# mailer = Mailer(app)

auth = Auth(app, db, user_model=User)

db.define_models([User, Post, Subscription])

app.pipeline = [
    SessionManager.cookies('b795-18a878ae9368', expire=4*60*60),
    db.pipe,
    auth.pipe,
]

auth_routes = auth.module(__name__)

from backend.controllers import *

# @auth_routes.after_login
# def after_login(form):
#     redirect(url('main.index'))
