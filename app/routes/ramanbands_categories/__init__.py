from flask import Blueprint

bp = Blueprint('ramanbands_categories', __name__)

from app.routes.ramanbands_categories import routes
