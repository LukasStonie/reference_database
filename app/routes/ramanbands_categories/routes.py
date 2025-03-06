import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from flask_babel import _

from app.forms.forms import RamanBandCategoryForm
from app.routes.ramanbands_categories import bp
from app.models.model import RamanBandCategory
from app.extensions import db

@bp.route('/')
@login_required
def index():
    categories = db.session.query(RamanBandCategory).all()
    print(categories)
    return render_template('resources/ramanband_categories/index.html', categoires=categories)

@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for raman bands, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new raman band
    """
    form = RamanBandCategoryForm()
    return render_template('resources/ramanband_categories/new.html', form=form)

@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new band category, only accessible for logged in users

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = RamanBandCategoryForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/ramanband_categories/new.html', form=form)
    # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            category = RamanBandCategory(name=form.name.data)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('ramanbands_categories.index'))
        except sqlalchemy.exc.IntegrityError:
            flash(_('Diese Kategorie existiert bereits'), 'danger')
            return render_template('resources/ramanband_categories/new.html', form=form)


@bp.route('/<category_id>/edit', methods=['GET'])
@login_required
def edit(category_id):
    """
        Edit page for band category, only accessible for logged in users

    Args:
        category_id (int): id of the category to be edited

    Returns:
        rendered template of the edit page, with the form for editing a band category
    """
    category = db.session.query(RamanBandCategory).filter(RamanBandCategory.id == category_id).first()
    print(category.name)
    form = RamanBandCategoryForm(obj=category)
    print(form.name.data)
    return render_template('resources/ramanband_categories/edit.html', form=form)


@bp.route('/<category_id>/edit', methods=['POST'])
@login_required
def edit_post(category_id):
    """
        Edits the band category, only accessible for logged in users

    Args:
        category_id (int): id of the category to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = RamanBandCategoryForm(request.form)
    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/ramanband_categories/edit.html', form=form)
        # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            category = db.session.query(RamanBandCategory).filter(RamanBandCategory.id == category_id).first()
            category.name = form.name.data
            db.session.commit()
            return redirect(url_for('ramanbands_categories.index'))
        except sqlalchemy.exc.IntegrityError:
            flash(_('Diese Kategorie existiert bereits'), 'danger')
            return render_template('resources/ramanband_categories/edit.html', form=form)
@bp.route('/<category_id>/delete')
@login_required
def delete(category_id):
    """
        Deletes the band category if not used in a compound, only accessible for logged in users

    Args:
        category_id (int): id of the category to be deleted

    Returns:
        redirects to the index page, with a flash message based on the success of the deletion
    """
    try:
        category = db.session.query(RamanBandCategory).filter(RamanBandCategory.id == category_id).first()
        db.session.delete(category)
        db.session.commit()
        flash(_("Kategorie wurde gelöscht"), 'success')
        return redirect(url_for('ramanbands_categories.index'))
    except sqlalchemy.exc.IntegrityError:
        flash(_('Diese Kategorie wird noch verwendet und kann daher nicht gelöscht werden.'), 'danger')
        return redirect(url_for('ramanbands_categories.index'))
    except:
        flash(_('Kategorie konnte nicht gelöscht werden. Probieren Sie es später erneut.'), 'danger')
        return redirect(url_for('ramanbands_categories.index'))