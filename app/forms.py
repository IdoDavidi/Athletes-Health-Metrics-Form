from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, SelectField, DateField
from wtforms.fields.datetime import TimeField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime


class AthleteForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    jersey_number = IntegerField('Jersey Number', validators=[DataRequired(), NumberRange(min=0)])
    date = DateField('Date', default=datetime.today, validators=[DataRequired()])
    sleep_hours = SelectField(
        'Hours of Sleep',
        choices=[('', 'Select...')] + [(str(i), str(i)) for i in [x * 0.5 for x in range(0, 29)]],
        coerce=lambda x: float(x) if x else None,
        validators=[DataRequired()])
    bed_time = TimeField('Time Went to Bed', validators=[DataRequired()])
    water_intake = SelectField("Yesterday's water intake (in Liters)",
                               choices=[('', 'Select...')] + [(str(i), str(i)) for i in
                                                              [x * 0.5 for x in range(0, 11)]],
                               coerce=lambda x: float(x) if x else None,
                               validators=[DataRequired()])
    breakfast = StringField('Breakfast', validators=[DataRequired()])
    mental_rating = SelectField('Mental Rating (1-10)',
                                choices=[('', 'Select...')] + [(str(i), str(i)) for i in range(1, 11)],
                                coerce=lambda x: int(x) if x else None,
                                validators=[DataRequired()])
    physical_rating = SelectField('Physical Rating (1-10)',
                                  choices=[('', 'Select...')] + [(str(i), str(i)) for i in range(1, 11)],
                                  coerce=lambda x: int(x) if x else None,
                                  validators=[DataRequired()])
    submit = SubmitField('Submit')
