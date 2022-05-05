# -*- coding: utf-8 -*-
__author__ = 'SirHades696'
__email__ = 'djnonasrm@gmail.com'

from flask import (
    Blueprint,
    render_template
)

bp = Blueprint('index',__name__)

@bp.route('/')
def index():
    return render_template('index/index.html')