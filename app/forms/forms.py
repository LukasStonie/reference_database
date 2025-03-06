"""
    Forms Module
"""
from datetime import datetime

from flask import g
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField, PasswordField, SelectField, SelectMultipleField, SubmitField, FieldList, FormField,
                     DateField)
from wtforms.fields.html5 import EmailField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional
from flask_babel import lazy_gettext as _l
from app.extensions import db


class SignupForm(FlaskForm):
    """
        WTForms class for the signup form

    Attributes:
        firstname: StringField, required, min 2, max 45

        lastname: StringField, required, min 2, max 60

        email: EmailField, required, min 2, max 60, email

        password: PasswordField, required, min 8, max 60, equal to password_repeat

        password_repeat: PasswordField, required, min 8, max 60
    """

    firstname = StringField(_l('Vorname'), validators=[InputRequired(), Length(min=2, max=45)])
    lastname = StringField(_l('Nachname'), validators=[InputRequired(), Length(min=2, max=60)])
    email = EmailField(_l('E-Mail'), validators=[InputRequired(), Length(min=2, max=60), Email()])
    password = PasswordField(_l('Passwort'), validators=[
        InputRequired(),
        Length(min=8, max=60),
        EqualTo('password_repeat', message=_l('Passwörter stimmen nicht überein'))])
    password_repeat = PasswordField(_l('Passwort wiederholen'),
                                    validators=[InputRequired(), Length(min=8, max=60)])


class LoginForm(FlaskForm):
    """
        WTForms class for the login form

    Attributes:
        email: EmailField, required, min 2, max 60, email

        password: PasswordField, required, min 8, max 60
    """
    email = EmailField(_l('E-Mail'), validators=[InputRequired(), Length(min=2, max=60), Email()])
    password = PasswordField(_l('Passwort'), validators=[InputRequired(), Length(min=8, max=60)])


class LensesForm(FlaskForm):
    """
        WTForms class for the lenses form

    Attributes:
        zoom: IntegerField, required

        numerical_aperture: IntegerField, required
    """
    zoom = IntegerField(_l('Zoom'), validators=[InputRequired(message=_l("Bitte geben Sie eine Vergößerung ein"))])
    numerical_aperture = IntegerField(_l('Numerische Apertur'),
                                      validators=[
                                          InputRequired(message=_l("Bitte geben Sie eine numerische Apertur ein"))])
    print("lenses form")
    print(numerical_aperture)


class LasersForm(FlaskForm):
    """
        WTForms class for the lasers form

    Attributes:
        wavelength: IntegerField, required
    """
    wavelength = IntegerField(_l('Wellenlänge [nm]'),
                              validators=[InputRequired(message=_l('Bitte geben Sie eine Wellenlänge an'))])


class AperturesForm(FlaskForm):
    """
        WTForms class for the apertures form

    Attributes:
        size: IntegerField, required
    """
    size = IntegerField(_l('Größe [µm]'), validators=[InputRequired(message=_l('Bitte geben Sie eine Größe an'))])


class SlidesForm(FlaskForm):
    """
        WTForms class for the slides form

    Attributes:
        name: StringField, required
    """
    name = StringField(_l('Bezeichnung'), validators=[InputRequired(message=_l('Bitte geben Sie eine Bezeichnung an'))])


class SpectralRangesForm(FlaskForm):
    """
        WTForms class for the spectral_ranges form

    Attributes:
        start: IntegerField, required

        end: IntegerField, required
    """
    start = IntegerField(label="Start [cm<sup>-1</sup>]",
                         validators=[InputRequired(message=_l('Bitte geben Sie einen Startwert an'))])
    end = IntegerField(_l('Ende [cm^-1]'), validators=[InputRequired(message=_l('Bitte geben Sie einen Endwert an'))])


class ResolutionsForm(FlaskForm):
    """
        WTForms class for the resolutions form

    Attributes:
        description: IntegerField, required
    """
    description = StringField(_l('Bezeichnung'),
                              validators=[InputRequired(message=_l('Bitte geben Sie eine Bezeichnung an'))])


class SpectralTypesForm(FlaskForm):
    """
        WTForms class for the spectral_types form

    Attributes:
        description: StringField, required
    """
    description = StringField(_l('Bezeichnung'),
                              validators=[InputRequired(message=_l('Bitte geben Sie eine Bezeichnung an'))])


class PreprocessingStepsForm(FlaskForm):
    """
        WTForms class for the preprocessing_steps form

    Attributes:
        name: StringField, required
    """
    name = StringField(_l('Bezeichnung'), validators=[InputRequired(message=_l('Bitte geben Sie eine Bezeichnung an'))])


class SubstratesForm(FlaskForm):
    """
        WTForms class for the substrates form

    Attributes:
        name: StringField, required

        instructions: FileField, optional
    """
    name = StringField(_l('Bezeichnung'), validators=[InputRequired(message=_l('Bitte geben Sie eine Bezeichnung an'))])
    instructions = FileField(_l('Anleitung'), validators=[])


class CompoundsForm(FlaskForm):
    """
        WTForms class for the compounds form

    Attributes:
        name: StringField, required

        coaddition: IntegerField, required

        integration_time: IntegerField, required

        laser_power: IntegerField, required

        description: StringField, optional

        lenses: SelectField, required

        lasers: SelectField, required

        apertures: SelectField, required

        slides: SelectField, required

        spectral_ranges: SelectField, required

        resolutions: SelectField, required

        substrates: SelectField, optional

        create: SubmitField

        create_and_add: SubmitField, used to distinguish between create and create_and_add_spectrum
    """
    name = StringField(_l('Bezeichnung'), validators=[InputRequired(message=_l('Bitte geben Sie eine Bezeichnung an'))])
    coaddition = IntegerField(_l('Koaddition'),
                              validators=[InputRequired(message=_l('Bitte geben Sie eine Koaddition an'))])
    integration_time = IntegerField(_l('Integrationszeit [ms]'),
                                    validators=[InputRequired(message=_l('Bitte geben Sie eine Integrationszeit an'))])
    laser_power = IntegerField(_l('Laserleistung [mW]'),
                               validators=[InputRequired(message=_l('Bitte geben Sie eine Laserleistung an'))])
    description = StringField(_l('Beschreibung'), validators=[])

    lenses = SelectField(_l('Objektiv'), validate_choice=False,
                         validators=[InputRequired(message=_l('Bitte wählen Sie ein Objektiv aus'))])
    lasers = SelectField(_l('Laser'), validate_choice=False,
                         validators=[InputRequired(message=_l('Bitte wählen Sie einen Laser aus'))])
    apertures = SelectField(_l('Apertur [µm]'), validate_choice=False,
                            validators=[InputRequired(message=_l('Bitte wählen Sie eine Apertur aus'))])
    slides = SelectField(_l('Objektträger'), validate_choice=False,
                         validators=[InputRequired(message=_l('Bitte wählen Sie einen Objektträger aus'))])
    spectral_ranges = SelectField(_l('Spektralbereich'), validate_choice=False,
                                  validators=[InputRequired(message=_l('Bitte wählen Sie einen Spektralbereich aus'))])
    resolutions = SelectField(_l('Auflösung'), validate_choice=False,
                              validators=[InputRequired(message=_l('Bitte wählen Sie eine Auflösung aus'))])
    substrates = SelectField(_l('Substrat'), validate_choice=False, validators=[])

    date_of_creation = DateField(_l('Erstellungsdatum'), format='%Y-%m-%d', validators=[Optional()])

    create = SubmitField(_l('Erstellen'))
    create_and_add = SubmitField(_l('Erstellen und Spektrum hinzufügen'), validators=[Optional()])


class SpectraForm(FlaskForm):
    """
        WTForms class for the spectra form

    Attributes:
        spectrum_type: RadioField, required

        preprocessing_steps: SelectMultipleField, optional
    """
    spectrum_type = RadioField(_l('Spektrumart'), validate_choice=False,
                               validators=[InputRequired(message=_l('Bitte wählen Sie einen Spektrumtyp aus'))])
    preprocessing_steps = SelectMultipleField(_l('Vorverarbeitung'), validate_choice=False, validators=[])


class SpectraEditForm(FlaskForm):
    """
        WTForms class for the spectra form

    Attributes:
        spectrum_type: RadioField, required

        preprocessing_steps: SelectMultipleField, optional

        new_spectrum: BooleanField, indicate if a new spectrum should be uploaded
    """
    spectrum_type = RadioField(_l('Spektrumart'), validate_choice=False,
                               validators=[InputRequired(message=_l('Bitte wählen Sie einen Spektrumtyp aus'))])
    preprocessing_steps = SelectMultipleField(_l('Vorverarbeitung'), validate_choice=False, validators=[])
    new_spectrum = BooleanField(_l('Spektrum austauschen'))


class IntensityForm(FlaskForm):
    """
        WTForms class for the intensities form

    Attributes:
        shorthand: StringField, required, min 1, max 3

        description: StringField, required
    """
    shorthand = StringField(_l('Kürzel'), validators=[InputRequired(message=_l('Bitte geben Sie ein Kürzel an')),
                                                      Length(min=1, max=3,
                                                             message=_l(
                                                                 "Das Kürzel darf maximal drei Zeichen lang sein"))])
    description = StringField(_l('Beschreibung'),
                              validators=[InputRequired(message=_l('Bitte geben Sie eine Beschreibung an'))])


class PeakForm(FlaskForm):
    """
        WTForms class for the peaks form

    Attributes:
        intensity: SelectField, required
    """
    intensities = SelectField(_l("Intensität"), validate_choice=False,
                              validators=[InputRequired(message=_l("Bitte wählen Sie eine Intesität aus."))])


class QueryForm(FlaskForm):
    """
        WTForms class for the query form

    Attributes:
        tolerance: DecimalField, required, default 10.0
    """
    tolerance = DecimalField(_l("Toleranz"), default=10.0,
                             validators=[InputRequired(message=_l("Bitte geben Sie einen Toleranzbereich an."))])


class RamanBandForm(FlaskForm):
    wavenumber = DecimalField(_l("Wellenzahl"),
                              validators=[InputRequired(message=_l("Bitte geben Sie eine Wellenzahl an."))])
    bandType = StringField(_l("Schwingungsart"),
                           validators=[InputRequired(message=_l("Bitte geben Sie eine Schwingungsart an."))])
    bandCategory = SelectField(_l("Kategorie"), validate_choice=False,
                               validators=[InputRequired(message=_l("Bitte geben Sie eine Kategorie an."))])
    bandAmplitude = SelectField(_l("Intensität"), validate_choice=False,
                                validators=[InputRequired(message=_l("Bitte geben Sie eine Amplitude an."))])
    author = StringField(_l("Autor"))
    doiLink = StringField(_l("DOI"))


class RamanBandCategoryForm(FlaskForm):
    name = StringField(_l("Kategorie"), validators=[InputRequired(message=_l("Bitte geben Sie eine Kategorie an."))])


class RamanBandQueryForm(FlaskForm):
    wavenumber = DecimalField(_l("Wellenzahl"), validators=[Optional()])
    bandCategory = SelectField(_l("Kategorie"), validate_choice=False, validators=[Optional()])
    bandType = StringField(_l("Schwingungsart"), validators=[Optional()])
