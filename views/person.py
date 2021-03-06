from flask import Blueprint, render_template
from models import Person, ContestDetail

PERSON_MOD = Blueprint('person_mod', __name__)


@PERSON_MOD.route('/conductor/')
def all_people() -> str:
    from sqlalchemy import func
    from database import get_db_session
    db_session = get_db_session()

    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '指揮'}
    ]

    conductors = db_session.query(Person, func.count(ContestDetail.id), func.count(func.NULLIF(ContestDetail.position != 1, True))).outerjoin(ContestDetail).group_by(Person.id)

    search_fields = ['conductor-name']
    search_hint = '指揮姓名'
    return render_template(
        'conductors.html',
        search_fields=search_fields,
        search_hint=search_hint,
        ascending=True,
        breadcrumb=breadcrumb,
        conductors=conductors)


@PERSON_MOD.route('/conductor/<conductor_id>')
def get_conductor_info(conductor_id: str) -> str:
    search_hint = ''

    conductor = Person.query.filter_by(id=conductor_id).first()
    contest_details = ContestDetail.query.filter_by(conductor_id=conductor_id).all()

    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'path': '/person/conductor/', 'name': '指揮'},
        {'name': conductor.name}
    ]

    return render_template(
        'conductor.html',
        search_hint=search_hint,
        ascending=True,
        conductor=conductor,
        contest_details=contest_details,
        breadcrumb=breadcrumb)
