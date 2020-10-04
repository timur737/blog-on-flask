from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '%8d7f!^fr#nc&)utq16@*1p_sl8gj)ltog3m#lffjwt=+#y9w1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:4057@localhost/jumpi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)

from project0 import models, routes

db.create_all()
