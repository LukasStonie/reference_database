from flask import Blueprint, g

bp = Blueprint('main', __name__, url_prefix='/<lang_code>')


@bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


from app.routes.main import routes
