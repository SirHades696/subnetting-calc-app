# -*- coding: utf-8 -*-
__author__ = 'SirHades696'
__email__ = 'djnonasrm@gmail.com'

from flask import (
    Blueprint,
    render_template, 
    request,
    flash
)

from app.subnetting.vlsm import VLSM

bp = Blueprint('vlsm',__name__,url_prefix='/vlsmcalc')

@bp.route('/sub')
def vlsmcalc():
    return render_template('vlsm_calc/vlsm_form.html')

@bp.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        ip = request.form.get('ip')
        mask = request.form.get('mask')
        net = ip + '/' + mask
        hosts = request.form.get('hosts').split(',')
        hosts = [i for i in hosts if i] #Removing whitespaces
        networks, tn, treq, alloc_p = VLSM.vlsm_calc(net, hosts)
        if isinstance(networks, dict):
            error=''
            if int(treq) > int(tn):
                error = 'Subnetting Failed'
            flash(error)
            return render_template('vlsm_calc/vlsm_view.html', networks=networks, net=net, tn=tn, treq=treq, alloc_p=alloc_p)
        else:
            networks = networks + ': ' + net
            flash(networks)
            return render_template('vlsm_calc/vlsm_form.html')
    return render_template('vlsm_calc/vlsm_form.html')
    