from flask import Blueprint, render_template
from models import ContestType, Contest, ContestDetail, TestPiece
import datetime

contest_mod = Blueprint('contest_mod', __name__)


@contest_mod.route('/moe/')
def all_contests_moe():
    from sqlalchemy import func
    from database import db_session

    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['parent'].append({'name': '比賽'})
    breadcrumb['current'] = {'name': '學生音樂比賽'}

    contests = db_session.query(ContestType, func.count(Contest.id)).outerjoin(Contest).group_by(ContestType.id).filter((ContestType.parent_id == 1) | (ContestType.id == 1))

    search_fields = ['contest-location']
    shortcut_options = []
    search_hint = '比賽名稱'
    return render_template(
        'contest-moe-list.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=True,
        contests=contests,
        breadcrumb=breadcrumb)


@contest_mod.route('/moe/<contest_type_id>')
def all_contests_moe_location(contest_type_id):
    contest = ContestType.query.filter_by(id=contest_type_id).first()

    contest.contests = Contest.query.filter_by(contest_type_id=contest.id).group_by(Contest.area_id, Contest.category, Contest.band_type).all()

    for c in contest.contests:
        c.champion = ContestDetail.query.join(Contest).join(ContestType).filter(ContestType.id == contest.id, Contest.area_id == c.area_id, Contest.band_type == c.band_type, ContestDetail.position == 1).order_by(Contest.date.desc()).first()

    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['parent'].append({'name': '比賽'})
    breadcrumb['parent'].append({'path': '/contest/moe/', 'name': '學生音樂比賽'})
    breadcrumb['current'] = {'name': contest.name}

    meta = dict()
    meta['has_area'] = True
    meta['has_category'] = True
    meta['contest_id'] = 'moe'

    search_fields = ['contest-group', 'contest-area']
    shortcut_options = ['北區', '東區', '西區', '南區', '高中', '國中', '國小']
    search_hint = '地域 / 組別'
    return render_template(
        'contest-group-list.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=True,
        breadcrumb=breadcrumb,
        contest=contest,
        meta=meta)


@contest_mod.route('/moe/<contest_type_id>/<area_id>/<band_type>/<category>')
def all_contests_moe_location_area(contest_type_id, area_id, band_type, category):
    contests = Contest.query.filter_by(contest_type_id=contest_type_id, area_id=area_id, band_type=band_type, category=category).all()

    for contest in contests:
        contest.year = contest.date.strftime('%Y')
        contest.test_pieces = TestPiece.query.filter(TestPiece.contests.any(id=contest.id)).all()

        champion_record = ContestDetail.query.filter_by(contest_id=contest.id, position=1).first()
        contest.champion = champion_record.band.name if champion_record else ''

        contest.url = '/contest/moe/{}/{}/{}/{}/{}'.format(contest_type_id, area_id, band_type, category, contest.year)

    # XXX: at least one band is required
    contest_name = contests[0].get_fullname(prefix=False, area=False, category=False, band_type=False)
    contest_area = contests[0].get_fullname(prefix=False, ctype=False)

    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['parent'].append({'name': '比賽'})
    breadcrumb['parent'].append({'path': '/contest/moe/', 'name': '學生音樂比賽'})
    breadcrumb['parent'].append({'path': '/contest/moe/{}'.format(contest_type_id), 'name': contest_name})
    breadcrumb['current'] = {'name': contest_area}

    search_fields = []
    shortcut_options = []
    search_hint = ''
    return render_template(
        'contest-history.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=False,
        breadcrumb=breadcrumb,
        contests=contests,
        contest_name=contest_name,
        contest_area=contest_area)


@contest_mod.route('/moe/<contest_type_id>/<area_id>/<band_type>/<category>/<year>')
def all_contests_moe_location_area_group_category_year(contest_type_id, area_id, band_type, category, year):
    contest = Contest.query.filter(Contest.contest_type_id == contest_type_id, Contest.area_id == area_id, Contest.band_type == band_type, Contest.category == category, Contest.date > datetime.datetime.strptime(year, '%Y'), Contest.date < datetime.datetime.strptime(str(int(year) + 1), '%Y')).first()

    contest.test_pieces = TestPiece.query.filter(TestPiece.contests.any(id=contest.id)).all()

    contest.teams = ContestDetail.query.filter_by(contest_id=contest.id).all()
    contest_name = contest.get_fullname(area=False, category=False, band_type=False)
    contest_area = contest.get_fullname(prefix=False, ctype=False)

    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['parent'].append({'name': '比賽'})
    breadcrumb['parent'].append({'path': '/contest/moe/', 'name': '學生音樂比賽'})
    breadcrumb['parent'].append({'path': '/contest/moe/%s' % contest_type_id, 'name': contest.get_fullname(prefix=False, area=False, category=False, band_type=False)})
    breadcrumb['parent'].append({'path': '/contest/moe/%s/%s/%s/%s' % (contest_type_id, area_id, band_type, category), 'name': contest_area})
    breadcrumb['current'] = {'name': year}

    search_fields = []
    shortcut_options = []
    search_hint = ''
    return render_template(
        'contest-detail.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=True,
        sortme=0,
        contest=contest,
        breadcrumb=breadcrumb,
        contest_name=contest_name,
        contest_area=contest_area)
