import sqlalchemy.exc
from flask import render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from flask_babel import _
from sqlalchemy import desc

from app.forms.forms import RamanBandForm, RamanBandQueryForm
from app.routes.ramanbands import bp
from app.models.model import RamanBands, RamanBandAssignment, RamanBandCategory, Intensity
from app.extensions import db


@bp.route('/')
@login_required
def index():
    bands = db.session.query(RamanBands).order_by(RamanBands.wavenumber).all()

    return render_template('resources/ramanbands/index.html', bands=bands)


def build_ramanband_form():
    categories = db.session.query(RamanBandCategory).all()
    intensities = db.session.query(Intensity).all()
    form = RamanBandForm()
    form.bandCategory.choices = [(c.id, c.name) for c in categories]
    form.bandAmplitude.choices = [(i.id, str(i.shorthand) + " (" + str(i.description) + ")") for i in intensities]
    return form


@bp.route('/new', methods=['GET'])
@login_required
def new():
    """
        Create page for raman bands, only accessible for logged in users

    Returns:
        rendered template of the new page, with the form for creating a new raman band
    """
    form = build_ramanband_form()
    return render_template('resources/ramanbands/new.html', form=form)


@bp.route('/new', methods=['POST'])
@login_required
def new_post():
    """
        Creates a new laser, only accessible for logged in users

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Create page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = RamanBandForm(request.form)
    categories = db.session.query(RamanBandCategory).all()
    intensities = db.session.query(Intensity).all()
    form.bandCategory.choices = [(c.id, c.name) for c in categories]
    form.bandAmplitude.choices = [(i.id, str(i.shorthand) + " (" + str(i.description) + ")") for i in intensities]

    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/ramanbands/new.html', form=form)
    # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            wavenumber = form.wavenumber.data
            bandType = form.bandType.data
            bandCategory = form.bandCategory.data
            bandAmplitude = form.bandAmplitude.data
            author = form.author.data
            doi = form.doiLink.data

            bandAssignment = RamanBandAssignment(bandType=bandType, bandCategoryId=bandCategory,
                                                 bandAmplitudeId=bandAmplitude, author=author, doiLink=doi)

            db.session.add(bandAssignment)
            db.session.commit()

            band = RamanBands(wavenumber=wavenumber, bandAssignmentId=bandAssignment.id)
            db.session.add(band)
            db.session.commit()

            return redirect(url_for('ramanband.index'))
        except sqlalchemy.exc.IntegrityError:
            flash(_('Diese Kategorie existiert bereits'), 'danger')
            return render_template('resources/ramanbands/new.html', form=form)


@bp.route('/<band_id>/edit', methods=['GET'])
@login_required
def edit(band_id):
    """
        Edit page for raman band, only accessible for logged in users

    Args:
        band_id (int): id of the band to be edited

    Returns:
        rendered template of the edit page, with the form for editing a band
    """
    band = db.session.query(RamanBands).filter(RamanBands.id == band_id).first()
    form = build_ramanband_form()
    form.doiLink.data = band.bandAssignment.doiLink
    form.author.data = band.bandAssignment.author
    form.bandAmplitude.data = str(band.bandAssignment.bandAmplitudeId)
    form.bandCategory.data = str(band.bandAssignment.bandCategoryId)
    form.bandType.data = band.bandAssignment.bandType
    form.wavenumber.data = band.wavenumber
    return render_template('resources/ramanbands/edit.html', form=form)


@bp.route('/<band_id>/edit', methods=['POST'])
@login_required
def edit_post(band_id):
    """
        Edits the raman band, only accessible for logged in users

    Args:
        band_id (int): id of the raman band to be edited

    Returns:
        based on the validation of the form, either redirects to this resources index page or
        renders the Edit page again with validation errors (WTForms) or integrity errors (SQL constraints)
    """
    # convert request.form to form object
    form = RamanBandForm(request.form)
    categories = db.session.query(RamanBandCategory).all()
    intensities = db.session.query(Intensity).all()
    form.bandCategory.choices = [(c.id, c.name) for c in categories]
    form.bandAmplitude.choices = [(i.id, str(i.shorthand) + " (" + str(i.description) + ")") for i in intensities]

    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        print(form.wavenumber.data)
        return render_template('resources/ramanbands/edit.html', form=form)
        # if the form is valid, create a new lens and redirect to the index page
    else:
        # if unique constraint is violated, inform the user
        try:
            ramanband = db.session.query(RamanBands).filter(RamanBands.id == band_id).first()
            bandAssignment = ramanband.bandAssignment

            ramanband.wavenumber = form.wavenumber.data

            bandAssignment.bandType = form.bandType.data
            bandAssignment.bandCategoryId = form.bandCategory.data
            bandAssignment.bandAmplitudeId = form.bandAmplitude.data
            bandAssignment.author = form.author.data
            bandAssignment.doiLink = form.doiLink.data

            db.session.commit()
            return redirect(url_for('ramanband.index'))
        except sqlalchemy.exc.IntegrityError:
            flash(_('Dieses Raman-Band existiert bereits'), 'danger')
            return render_template('resources/ramanbands/edit.html', form=form)


@bp.route('/<band_id>/delete')
@login_required
def delete(band_id):
    """
        Deletes the band  if not used in a compound, only accessible for logged in users

    Args:
        band_id (int): id of the band to be deleted

    Returns:
        redirects to the index page, with a flash message based on the success of the deletion
    """
    try:
        category = db.session.query(RamanBands).filter(RamanBands.id == band_id).first()
        db.session.delete(category)
        db.session.commit()
        flash(_("Raman-Band wurde gelöscht"), 'success')
        return redirect(url_for('ramanband.index'))
    except sqlalchemy.exc.IntegrityError:
        flash(_('Dieses Raman-Band wird noch verwendet und kann daher nicht gelöscht werden.'), 'danger')
        return redirect(url_for('ramanband.index'))
    except:
        flash(_('Raman-Band konnte nicht gelöscht werden. Probieren Sie es später erneut.'), 'danger')
        return redirect(url_for('ramanband.index'))


def build_ramanbandquery_form():
    categories = db.session.query(RamanBandCategory).all()
    intensities = db.session.query(Intensity).all()
    form = RamanBandQueryForm()
    categories = [(c.id, c.name) for c in categories]
    categories.insert(0, (0, 'Alle'))
    form.bandCategory.choices = categories
    return form


@bp.route('/query', methods=['GET'])
@login_required
def query():
    """
            Query page for raman bands, only accessible for logged in users

        Returns:
            rendered template of the query page, with the form for querying a raman band
        """
    form = build_ramanbandquery_form()

    return render_template('resources/ramanbands/query.html', form=form, initial=True)


@bp.route('/query', methods=['POST'])
@login_required
def query_post():
    """
    Queries the database for raman bands that match the filters, only accessible for logged in users

    Returns:
        a rendered template of the query page, with the form for querying a raman band and the results of the query
        """
    # convert request.form to form object
    form = RamanBandQueryForm(request.form)
    categories = db.session.query(RamanBandCategory).all()

    categories = [(c.id, c.name) for c in categories]
    categories.insert(0, (0, 'Alle'))
    form.bandCategory.choices = categories


    # if the form is not valid, redirect to the new page and pass the values from the form
    if not form.validate():
        return render_template('resources/ramanbands/query.html', form=form, initial=True)
        # if the form is valid, create a new lens and redirect to the index page
    else:
        # query the database using the provided filter values
        wavenumber = form.wavenumber.data
        bandCategory = form.bandCategory.data
        bandType = form.bandType.data

        queryfilter = db.session.query(RamanBands).join(RamanBandAssignment)

        if wavenumber:
            queryfilter = queryfilter.filter(RamanBands.wavenumber == wavenumber)

        if bandType:
            queryfilter = queryfilter.filter(RamanBandAssignment.bandType.contains(bandType))

        if bandCategory != '0':  # 0 is the value for "all"
            queryfilter = queryfilter.filter(RamanBandAssignment.bandCategoryId == bandCategory)

        bands = queryfilter.order_by(RamanBands.wavenumber).all()

        return render_template('resources/ramanbands/query.html', form=form, bands=bands, initial=False)
