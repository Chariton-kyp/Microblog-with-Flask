from flask import Blueprint

bp = Blueprint('login', __name__, template_folder='templates')

from app.forum.login import routes