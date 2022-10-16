from flask import Blueprint

main_forum = Blueprint('main_forum', __name__, template_folder='templates')

from app.forum.main_forum import routes