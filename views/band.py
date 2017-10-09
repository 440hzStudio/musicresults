from collections import defaultdict
from typing import List, DefaultDict

from flask import Blueprint, render_template
from models import Constant, Band, ContestDetail, Contest

BAND_MOD = Blueprint('band_mod', __name__)


def get_winning_records() -> defaultdict:
    winning_records: DefaultDict[str, List[str]] = defaultdict(list)
    contests = Contest.query.all()
    for contest in contests:
        record = ContestDetail.query.filter_by(position=1, contest_id=contest.id).join(Contest).order_by(Contest.date.desc()).first()
        if record is not None:
            winning_records[record.band_id].append(record.contest.get_fullname(prefix=False))
    return winning_records


@BAND_MOD.route('/')
def get_all_band_list() -> str:
    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '樂團'}
    ]

    winning_records = get_winning_records()

    all_bands = Band.query.all()
    for band in all_bands:
        band.contest_count = ContestDetail.query.filter_by(band_id=band.id).count()
        band.trophies = winning_records[band.id]

    search_fields = ['band-name', 'band-type']
    search_hint = '樂團名 / 樂團類型'
    return render_template(
        'bands.html',
        search_fields=search_fields,
        shortcut_options=Constant.BAND_TYPE,
        search_hint=search_hint,
        ascending=True,
        breadcrumb=breadcrumb,
        bands=all_bands)


@BAND_MOD.route('/<band_id>')
def get_band_detail(band_id: str) -> str:
    band = Band.query.filter_by(id=band_id).first()
    band.trophies = get_winning_records()[band.id]
    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'path': '/band/', 'name': '樂團'},
        {'name': band.name}
    ]

    band.contest_details = ContestDetail.query.filter_by(band_id=band.id).join(Contest).order_by(Contest.date.desc()).all()

    return render_template(
        'band.html',
        breadcrumb=breadcrumb,
        band=band)
