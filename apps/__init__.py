# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_wtf import CSRFProtect

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config["DATABASE"] = 'apps/database.db'
app.config["SECRET_KEY"] = '\xa2\xda\x01\xdb\xa7\x03\xeb\x9c-\xaec\xca\xea\xd1\xa7\x14\xe1\xd34\xd9\xa8\xcf\x99'
app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, UPLOAD_FOLDER)
csrf = CSRFProtect(app)

import apps.views
