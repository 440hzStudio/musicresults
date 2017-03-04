# -*- coding: utf-8 -*-
from flask import Flask, url_for, redirect, session, flash
from datetime import timedelta
import flask_login

from database import init_db
from views.user import user_mod, set_hash
from models import User
from views.band import band_mod
from views.contest import contest_mod
from views.contribute import contribute_mod
from views.index import index_mod
from views.person import person_mod
from views.testpiece import testpiece_mod
from views.venue import venue_mod

app = Flask(__name__)
app.config.from_pyfile('musicresults.cfg')
init_db(app)
set_hash(app.config.get('PWD_SALT'))

app.register_blueprint(band_mod, url_prefix='/band')
app.register_blueprint(contest_mod, url_prefix='/contest')
app.register_blueprint(contribute_mod, url_prefix='/contribute')
app.register_blueprint(index_mod)
app.register_blueprint(person_mod, url_prefix='/person')
app.register_blueprint(testpiece_mod, url_prefix='/test-piece')
app.register_blueprint(user_mod, url_prefix='/user')
app.register_blueprint(venue_mod, url_prefix='/venue')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    from database import db_session
    db_session.remove()


@login_manager.user_loader
def user_loader(username):
    uid = '_'.join(username.split('_')[1:])
    user = None

    if username.startswith('user'):
        user = User.query.filter_by(username=uid).first()
    elif username.startswith('tester'):
        user = Tester.query.filter_by(id=uid).first()

    return user


@app.before_request
def make_session_permanent():
    session.permanent = True
    if flask_login.current_user.is_authenticated and flask_login.current_user.is_admin():
        app.permanent_session_lifetime = timedelta(minutes=60)
    else:
        app.permanent_session_lifetime = timedelta(minutes=15)


@app.errorhandler(401)
def not_authorized(e):
    flash('請重新登入', 'info')
    return redirect(url_for('test_mod.login'))


if __name__ == '__main__':
    if app.config.get('RUNNING_MODE') == 'debug':
        app.run(
            host=app.config.get('HOST', 'localhost'),
            port=app.config.get('PORT', 8080)
        )
    else:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(app.config.get('PORT', 8080))
        IOLoop.instance().start()
