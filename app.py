from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

APPOINTMENTS_FILE = 'appointments.json'

def load_appointments():
    try:
        with open(APPOINTMENTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, 'w') as file:
        json.dump(appointments, file, indent=4)

@app.route('/')
def index():
    appointments = load_appointments()
    return render_template('index.html', appointments=appointments)

@app.route('/add', methods=['POST'])
def add_appointment():
    title = request.form['title']
    date_str = request.form['date']
    time_str = request.form['time']
    
    try:
        datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        appointments = load_appointments()
        appointments.append({
            'title': title,
            'date': date_str,
            'time': time_str
        })
        save_appointments(appointments)
        return redirect(url_for('index'))
    except ValueError:
        return "Invalid date or time format. Please try again.", 400

@app.route('/delete/<int:appointment_id>')
def delete_appointment(appointment_id):
    appointments = load_appointments()
    if 0 <= appointment_id < len(appointments):
        del appointments[appointment_id]
        save_appointments(appointments)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
