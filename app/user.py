from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('user', __name__, url_prefix='/user')

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


