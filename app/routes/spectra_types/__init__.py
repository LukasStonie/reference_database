from flask import Blueprint, g

bp = Blueprint('spectra_types', __name__)

@bp.url_defaults
def add_language_code(endpoint, values):
    if 'lang_code' not in g:
        g.lang_code = 'de'  # or your default language
    values.setdefault('lang_code', g.lang_code)


@bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

from app.routes.spectra_types import routes