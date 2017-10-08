from typing import List, Tuple, Optional

from flask import Blueprint, render_template
from models import Venue, Contest

VENUE_MOD = Blueprint('venue_mod', __name__)


@VENUE_MOD.route('/')
def all_venues() -> str:
    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['current'] = {'name': '場地'}

    venues = Venue.query.all()
    for venue in venues:
        venue.contest_count = Contest.query.filter_by(venue_id=venue.id).count()

    search_fields = ['venue-name', 'venue-location']
    shortcut_options: List[str] = []  # ['北區', '中區', '南區', '海外']
    search_hint = '場地名稱 / 城市'
    return render_template(
        'venues.html',
        search_fields=search_fields,
        shortcut_options=shortcut_options,
        search_hint=search_hint,
        ascending=True,
        breadcrumb=breadcrumb,
        venues=venues)


@VENUE_MOD.route('/<venue_id>')
def get_venue_detail(venue_id: str) -> Tuple[str, Optional[int]]:
    if not venue_id.isdigit():
        return render_template(
            'error.html',
            title='Invalid venue ID',
            reason=f'[{venue_id}] is not a valid format.'), 400

    venue = Venue.query.filter_by(id=venue_id).first()
    contest_record = Contest.query.filter_by(venue_id=venue_id).all()

    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['parent'].append({'path': '/venue/', 'name': '場地'})
    breadcrumb['current'] = {'name': venue.name}

    return render_template(
        'venue.html',
        ascending=False,
        breadcrumb=breadcrumb,
        venue=venue,
        contests=contest_record)
