from flask import Blueprint, render_template
import flask_login

INDEX_MOD = Blueprint('index_mod', __name__)


@INDEX_MOD.route('/')
def index() -> str:
    return render_template(
        'index.html',
        current_user=flask_login.current_user)
