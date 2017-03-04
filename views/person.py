from flask import Blueprint, render_template
from models import Person, ContestDetail

person_mod = Blueprint('person_mod', __name__)


@person_mod.route('/conductor/')
def all_people():
    from sqlalchemy import func
    from database import db_session
    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['current'] = {'name': '指揮'}

    conductors = db_session.query(Person, func.count(ContestDetail.id), func.count(func.NULLIF(ContestDetail.position != 1, True))).outerjoin(ContestDetail).group_by(Person.id)

    search_fields = ['conductor-name']
    shortcut_options = []
    search_hint = '指揮姓名'
    return render_template(
        'conductors.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=True,
        breadcrumb=breadcrumb,
        conductors=conductors)


@person_mod.route('/conductor/<conductor_id>')
def conductor_info(conductor_id):
    search_fields = []
    shortcut_options = []
    search_hint = ''

    conductor = Person.query.filter_by(id=conductor_id).first()
    contest_details = ContestDetail.query.filter_by(conductor_id=conductor_id).all()

    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['parent'].append({'path': '/person/conductor/', 'name': '指揮'})
    breadcrumb['current'] = {'name': conductor.name}

    return render_template(
        'conductor.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=True,
        conductor=conductor,
        contest_details=contest_details,
        breadcrumb=breadcrumb)
