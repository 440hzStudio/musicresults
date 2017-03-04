from flask import Blueprint, render_template
import flask_login
index_mod = Blueprint('index_mod', __name__)


@index_mod.route('/')
def index():
    return render_template(
        'index.html',
        current_user=flask_login.current_user)
