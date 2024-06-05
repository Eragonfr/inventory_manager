from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('project', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT id, name, total_count'
        ' FROM item'
        ' ORDER BY id DESC'
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
            db.commit()
            return redirect(url_for('inventory.index'))

    return render_template('inventory/update.html', item=item)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_item(id)
    db = get_db()
    db.execute('DELETE FROM item WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('inventory.index'))
