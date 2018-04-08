# -*- coding: utf-8 -*-

from flask import Flask
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config["DATABASE"] = 'apps/database.db'
app.config["SECRET_KEY"] = '\xa2\xda\x01\xdb\xa7\x03\xeb\x9c-\xaec\xca\xea\xd1\xa7\x14\xe1\xd34\xd9\xa8\xcf\x99'
csrf = CSRFProtect(app)

import apps.views
