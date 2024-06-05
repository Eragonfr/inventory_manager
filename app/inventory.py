from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('inventory', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT item.id, name, total_count, username, date'
        ' FROM item'
        ' JOIN item_edition ON item.id = item_edition.item_id'
        ' JOIN user ON item_edition.by_user = user.id'
        ' GROUP BY item.id HAVING date = MIN(date)'
        ' ORDER BY item.id DESC'
    ).fetchall()
    return render_template('inventory/index.html', items=items)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        count = request.form['count']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO item (name, total_count)'
                ' VALUES (?, ?)',
                (name, count)
            )
            db.execute(
                'INSERT INTO item_edition (item_id, by_user, comment)'
                ' VALUES (last_insert_rowid(), ?, ?)',
                (g.user['id'], "Ajout de l'item")
            )
            db.commit()
            return redirect(url_for('inventory.index'))

    return render_template('inventory/create.html')

def get_item(id):
    item = get_db().execute(
        'SELECT id, name, total_count'
        ' FROM item'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if item is None:
        abort(404, f"Item id {id} doesn't exist.")

#    if check_author and post['author_id'] != g.user['id']:
#        abort(403)

    return item

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    item = get_item(id)

    if request.method == 'POST':
        name = request.form['name']
        count = request.form['count']
        comment = request.form['comment']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE item SET name = ?, total_count = ?'
                ' WHERE id = ?',
                (name, count, id)
            )
            db.execute(
                'INSERT INTO item_edition (item_id, by_user, comment)'
                ' VALUES (?, ?, ?)',
                (id, g.user['id'], comment)
            )
            db.commit()
            return redirect(url_for('inventory.index'))

    return render_template('inventory/update.html', item=item)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_item(id)
    db = get_db()
    db.execute('DELETE FROM item_edition WHERE item_id = ?', (id,))
    db.execute('DELETE FROM item_usage_history WHERE item_id = ?', (id,))
    db.execute('DELETE FROM item WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))
