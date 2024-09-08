import os
import pandas as pd
from flask import render_template, request, redirect, flash, jsonify
from datetime import datetime, timedelta
from app import app
from app.forms import AthleteForm
from flask import json

# Directory to store player data
PLAYER_DATA_DIR = 'player_data'

# Ensure the player data directory exists
if not os.path.exists(PLAYER_DATA_DIR):
    os.makedirs(PLAYER_DATA_DIR)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = AthleteForm()

    if form.validate_on_submit():
        full_name = form.full_name.data
        jersey_number = form.jersey_number.data
        date = datetime.today().strftime('%Y-%m-%d')
        sleep_hours = form.sleep_hours.data
        bed_time = form.bed_time.data
        water_intake = form.water_intake.data
        breakfast = form.breakfast.data
        mental_rating = form.mental_rating.data
        physical_rating = form.physical_rating.data

        # Create the filename for the player using the full name and jersey number
        filename = f"{full_name}_#{jersey_number}.csv"
        file_path = os.path.join(PLAYER_DATA_DIR, filename)

        # Check if a CSV file already exists for the player
        if os.path.exists(file_path):
            # Load existing data and check if there's an entry for today
            df = pd.read_csv(file_path)
            if date in df['Date'].values:
                flash("You have already submitted data for today!")
                # Option to redirect to data page
                return render_template('duplicate_submission.html', jersey_number=jersey_number)
        else:
            # Create a new DataFrame if the file doesn't exist
            df = pd.DataFrame(
                columns=['Date', 'Hours of Sleep', 'Time Went to Bed', 'Water Intake', 'Breakfast', 'Mental Rating',
                         'Physical Rating'])

        # Append the new data to the DataFrame
        new_data = {
            'Date': date,
            'Hours of Sleep': sleep_hours,
            'Time Went to Bed': bed_time,
            'Water Intake': water_intake,
            'Breakfast': breakfast,
            'Mental Rating': mental_rating,
            'Physical Rating': physical_rating
        }
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        # Save the updated data back to the CSV file
        df.to_csv(file_path, index=False)

        flash('Data submitted successfully!')
        return redirect(f'/player_data/{jersey_number}')

    return render_template('form.html', form=form)


@app.route('/player_data/<jersey_number>', methods=['GET'])
def player_data(jersey_number):
    # Find the CSV file for the player based on jersey number
    for filename in os.listdir(PLAYER_DATA_DIR):
        if jersey_number in filename:
            file_path = os.path.join(PLAYER_DATA_DIR, filename)
            player_name = filename.replace('.csv', '').replace(f'_{jersey_number}', '')
            break
    else:
        flash(f"No data found for jersey number {jersey_number}")
        return redirect('/')

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime and format it to show only the date
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # Format 'Time Went to Bed' to remove seconds
    df['Time Went to Bed'] = pd.to_datetime(df['Time Went to Bed']).dt.strftime('%H:%M')

    # Calculate the past 3 days and last week averages
    today = datetime.today().date()
    last_3_days = today - timedelta(days=3)
    last_week = today - timedelta(days=7)

    # Filter the data for the last 3 days and the last week
    last_3_days_data = df[df['Date'] >= last_3_days]
    last_week_data = df[df['Date'] >= last_week]

    # Calculate averages for each metric except 'Breakfast'
    last_3_days_avg = last_3_days_data[['Hours of Sleep', 'Water Intake', 'Mental Rating', 'Physical Rating']].mean().to_dict()
    last_week_avg = last_week_data[['Hours of Sleep', 'Water Intake', 'Mental Rating', 'Physical Rating']].mean().to_dict()

    # Render the results in a template
    return render_template('player_data.html',
                           jersey_number=jersey_number,
                           player_name=player_name,
                           player_data=df.to_dict(orient='records'),
                           last_3_days_avg=last_3_days_avg,
                           last_week_avg=last_week_avg)


@app.route('/get_data/<jersey_number>', methods=['GET'])
def get_data(jersey_number):
    # Find the CSV file for the player based on jersey number
    for filename in os.listdir(PLAYER_DATA_DIR):
        if jersey_number in filename:
            file_path = os.path.join(PLAYER_DATA_DIR, filename)
            break
    else:
        return jsonify({"error": "Player not found"})

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime and ensure proper formatting
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    player_name = filename.split('_')[1].split('.')[0]

    # Calculate averages for the last 3 days and last week
    today = datetime.today()
    last_3_days = today - timedelta(days=3)
    last_week = today - timedelta(days=7)

    # Filter the data for the last 3 days and the last week
    last_3_days_data = df[df['Date'] >= last_3_days.strftime('%Y-%m-%d')]
    last_week_data = df[df['Date'] >= last_week.strftime('%Y-%m-%d')]

    # Calculate averages for each metric except 'Breakfast'
    last_3_days_avg = last_3_days_data[['Hours of Sleep', 'Water Intake', 'Mental Rating', 'Physical Rating']].mean().to_dict()
    last_week_avg = last_week_data[['Hours of Sleep', 'Water Intake', 'Mental Rating', 'Physical Rating']].mean().to_dict()

    # Render the player_data.html template with the calculated data
    return render_template(
        'player_data.html',
        jersey_number=jersey_number,
        player_name=player_name,
        player_data=df.to_dict(orient='records'),
        last_3_days_avg=last_3_days_avg,
        last_week_avg=last_week_avg
    )


