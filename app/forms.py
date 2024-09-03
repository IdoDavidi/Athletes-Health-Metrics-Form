from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import TimeField, SelectField


class AthleteForm(FlaskForm):
    sleep_hours = SelectField(
        'Hours of Sleep',
        choices=[('', 'Select...')] + [(str(i), str(i)) for i in [x * 0.5 for x in range(0, 29)]],
        coerce=lambda x: float(x) if x else None,
        validators=[DataRequired()])
    bed_time = TimeField('Time Went to Bed', validators=[DataRequired()])
    water_intake = SelectField("Yesterday's water intake",
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
