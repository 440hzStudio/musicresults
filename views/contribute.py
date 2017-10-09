from flask import Blueprint, render_template, flash, request
from models import ContestType
# import flask_login
CONTRIBUTE_MOD = Blueprint('contribute_mod', __name__)


@CONTRIBUTE_MOD.route('/', methods=['GET', 'POST'])
def contribute() -> str:
    breadcrumb = [
        {'path': '/', 'name': '首頁'},
        {'name': '貢獻'}
    ]

    detail_items = ['band', 'conductor', 'testpiece', 'ownchoice', 'points', 'ranking', 'order', 'misc']

    if request.method == 'POST':
        detail_lists = {}
        for item in detail_items:
            detail_lists[item] = request.form.getlist('%s[]' % item)

        for i in range(len(detail_lists[detail_items[0]])):
            print(i)
            for detail in detail_lists:
                print(detail, detail_lists[detail][i])
            print()
        flash('成功新增資料', 'success')

    all_contest_categories = list()

    categories = ContestType.query.filter_by(parent_id=None).all()
    for category in categories:
        contests = ContestType.query.filter((ContestType.parent_id == category.id) | (ContestType.id == category.id)).all()
        category = {'name': category.name, 'contests': {contest_type.id: contest_type.name for contest_type in contests}}
        all_contest_categories.append(category)

    return render_template(
        'contribute.html',
        breadcrumb=breadcrumb,
        detail_items='\"' + '\", \"'.join(detail_items) + '\"',
        all_contest_categories=all_contest_categories)
