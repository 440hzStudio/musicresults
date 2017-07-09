# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from database import db_session
import datetime
import hashlib
import binascii
from validate_email import validate_email
import flask_login
from models import User, Constant

USER_MOD = Blueprint('user_mod', __name__)
password_hash = None


def set_hash(hash):
    global password_hash
    password_hash = hash


def hash_password(password):
    dk = hashlib.pbkdf2_hmac(
        'sha256',
        bytearray(password, 'ascii'),
        bytearray(password_hash, 'ascii'),
        100000)
    return binascii.hexlify(dk).decode('ascii')


@USER_MOD.route('/info', methods=['GET', 'POST'])
@flask_login.login_required
def info():
    if not flask_login.current_user.is_teacher():
        return '403 Forbidden.', 403

    if request.method == 'POST':
        user = flask_login.current_user
        status = ''
        messages = []
        url = ''

        try:
            if request.form['password'] != request.form['re_password']:
                messages.append(('密碼不符', 'danger'))

            if not validate_email(request.form['email']):
                messages.append(('email 格式不符', 'danger'))

            if not request.form['phone1'] or not request.form['phone2']:
                messages.append(('請輸入學校聯絡電話', 'danger'))

            if any(not digit.isdigit() for digit in request.form['phone1'] + request.form['phone2'] + request.form['phone3'] + request.form['cellphone']):
                messages.append(('電話號碼不可包含非數字', 'danger'))

            if 'school' not in request.form or not request.form['school']:
                messages.append(('請選擇學校', 'danger'))

            if messages:
                raise Exception

            if request.form['password']:
                user.password = hash_password(request.form['password'])
            user.email = request.form['email']
            user.work_phone = '%s.%s.%s' % (
                request.form['phone1'], request.form['phone2'], request.form['phone3'])
            user.cell_phone = request.form['cellphone']
            user.school_id = request.form['school']
        except Exception:
            status = 'error'
        else:
            db_session.commit()
            status = 'ok'
            flash('更新成功', 'success')
            url = url_for('user_mod.info')
        return jsonify(status=status, messages=messages, url=url)

    return render_template(
        'user_info.html',
        class_level=Constant.class_level,
        current_user=flask_login.current_user
    )


@USER_MOD.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        status = ''
        messages = []
        url = ''

        try:
            if not request.form['name']:
                messages.append(('請輸入姓名', 'danger'))
            elif any(char.isdigit() for char in request.form['name']):
                messages.append(('姓名不可包含數字', 'danger'))

            if not request.form['username']:
                messages.append(('請輸入使用者帳號', 'danger'))

            if not request.form['password']:
                messages.append(('請輸入密碼', 'danger'))
            elif request.form['password'] != request.form['re_password']:
                messages.append(('密碼不符', 'danger'))

            if not validate_email(request.form['email']):
                messages.append(('email 格式不符', 'danger'))

            if not request.form['phone1'] or not request.form['phone2']:
                messages.append(('請輸入學校聯絡電話', 'danger'))

            if any(not digit.isdigit() for digit in request.form['phone1'] + request.form['phone2'] + request.form['phone3'] + request.form['cellphone']):
                messages.append(('電話號碼不可包含非數字', 'danger'))

            if 'school' not in request.form or not request.form['school']:
                messages.append(('請選擇學校', 'danger'))

            if messages:
                raise Exception

            user = User(request.form['username'], request.form['email'])
            user.realname = request.form['name']
            user.password = hash_password(request.form['password'])
            user.work_phone = '%s.%s.%s' % (
                request.form['phone1'], request.form['phone2'], request.form['phone3'])
            user.cell_phone = request.form['cellphone']
            user.school_id = request.form['school']
            user.create_time = datetime.datetime.now()
            user.type = 'teacher'
        except Exception:
            status = 'error'
        else:
            db_session.add(user)
            db_session.commit()
            status = 'ok'
            flash('註冊成功', 'success')
            url = url_for('user_mod.login')
        return jsonify(status=status, messages=messages, url=url)
    else:
        return render_template(
            'user_register.html',
            class_level=Constant.class_level,
            current_user=flask_login.current_user
        )


@USER_MOD.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if flask_login.current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template(
            'user_login.html',
            class_level=Constant.class_level,
            current_user=flask_login.current_user
        )

    status = ''
    messages = []
    url = ''

    username = request.form['username'].strip()
    user = User.query.filter_by(username=username).first()

    if user and user.password == hash_password(request.form['password']):
        flask_login.login_user(user)
        status = 'ok'
        flash('成功登入', 'success')
        url = url_for('class_mod.list')

    else:
        status = 'error'
        messages.append(('認證失敗 請檢查帳號密碼是否正確', 'danger'))
    return jsonify(status=status, messages=messages, url=url)


@USER_MOD.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('news_mod.list'))


def is_user_exists(username):
    if User.query.filter_by(username=username).all():
        return True
    return False


@USER_MOD.route('/exists/<username>')
def exists(username):
    return jsonify(is_user_exists(username))
