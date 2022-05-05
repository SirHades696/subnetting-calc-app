# -*- coding: utf-8 -*-
__author__ = 'SirHades696'
__email__ = 'djnonasrm@gmail.com'

from flask import (
    Blueprint,
    render_template, 
    request,
    flash
)

from app.subnetting.subnetting import Subnetting

bp = Blueprint('ipcalc',__name__,url_prefix='/ipcalc')

@bp.route('/sub')
def ipcalc():
    return render_template('ip_subnetting/subnetting_form.html')

@bp.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        ip = request.form.get('ip')
        mask = request.form.get('mask')
        net = ip + '/' + mask
        values = Subnetting.subnetting_calc(net)
        if isinstance(values, list):
            return render_template('ip_subnetting/subnetting_view.html', values=values, net=net)
        else:
            values = values + ': ' + ip
            flash(values)
            return render_template('ip_subnetting/subnetting_form.html')
    return render_template('ip_subnetting/subnetting_form.html')