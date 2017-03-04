from flask import Blueprint, render_template, flash, request
import flask_login
contribute_mod = Blueprint('contribute_mod', __name__)


@contribute_mod.route('/', methods=['GET', 'POST'])
def contribute():
    breadcrumb = dict()
    breadcrumb['parent'] = [{'path': '/', 'name': '首頁'}]
    breadcrumb['current'] = {'name': '貢獻'}

    detail_items = ['band', 'conductor', 'testpiece', 'ownchoice', 'points', 'ranking', 'order', 'misc']

    if request.method == 'POST':
        detail_lists = {}
        for d in detail_items:
            detail_lists[d] = request.form.getlist('%s[]' % d)

        for i in range(len(detail_lists[detail_items[0]])):
            print(i)
            for d in detail_lists:
                print(d, detail_lists[d][i])
            print()
        flash('成功新增資料', 'success')

    return render_template(
        'contribute.html',
        breadcrumb=breadcrumb,
        detail_items='\"' + '\", \"'.join(detail_items) + '\"')
