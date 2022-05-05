# -*- coding: utf-8 -*-
__author__ = 'SirHades696'
__email__ = 'djnonasrm@gmail.com'

from flask import Flask
import secrets

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = secrets.token_hex(20)      
    )
    
    from . import index
    from . import ip_calc
    from . import vlsm_calc
    
    app.register_blueprint(index.bp)
    app.register_blueprint(ip_calc.bp)
    app.register_blueprint(vlsm_calc.bp)
    
    return app