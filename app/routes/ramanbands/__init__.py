from flask import Blueprint

bp = Blueprint('ramanband', __name__)

from app.routes.ramanbands import routes
