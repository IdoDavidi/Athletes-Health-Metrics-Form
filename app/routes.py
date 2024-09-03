from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import AthleteForm


@app.route('/', methods=['GET', 'POST'])
def form():
    form = AthleteForm()
    if form.validate_on_submit():
        # You can handle the form data here
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('form'))
    return render_template('form.html', title='Daily Athlete Form', form=form)
