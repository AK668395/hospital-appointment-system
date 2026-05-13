from flask import Flask, render_template, request, redirect, session
import sqlite3
import random
from chatbot.bot import get_bot_response

app = Flask(__name__)
app.secret_key = 'hospital_secret_key'


# DATABASE CONNECTION

def connect_db():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn


# CREATE DATABASE TABLES

conn = connect_db()

# APPOINTMENTS TABLE
conn.execute('''
CREATE TABLE IF NOT EXISTS appointments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_name TEXT,

    doctor_name TEXT,

    appointment_date TEXT,

    appointment_time TEXT,

    status TEXT DEFAULT 'Pending'
)
''')

# USERS TABLE
conn.execute('''
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    password TEXT
)
''')

conn.commit()
conn.close()


# HOME PAGE

@app.route('/')
def home():
    return render_template('index.html')


# ADMIN LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = ''

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':

            session['admin'] = True

            return redirect('/admin')

        else:
            error = 'Invalid Username or Password'

    return render_template(
        'login.html',
        error=error
    )


# LOGOUT

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')


# PATIENT SIGNUP

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = connect_db()

        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect('/patient_login')

    return render_template('signup.html')


# PATIENT LOGIN

@app.route('/patient_login', methods=['GET', 'POST'])
def patient_login():

    error = ''

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = connect_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:

            session['patient'] = username

            return redirect('/appointment')

        else:

            error = 'Invalid Credentials'

    return render_template(
        'patient_login.html',
        error=error
    )


# BOOK APPOINTMENT

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():

    if 'patient' not in session:

        return redirect('/patient_login')

    if request.method == 'POST':

        patient = request.form['patient_name']
        doctor = request.form['doctor_name']
        date = request.form['appointment_date']
        time = request.form['appointment_time']

        conn = connect_db()

        conn.execute('''
        INSERT INTO appointments
        (
            patient_name,
            doctor_name,
            appointment_date,
            appointment_time
        )

        VALUES (?, ?, ?, ?)
        ''', (patient, doctor, date, time))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('appointment.html')


# ADMIN DASHBOARD

@app.route('/admin')
def admin():

    if 'admin' not in session:

        return redirect('/login')

    conn = connect_db()

    appointments = conn.execute(
        'SELECT * FROM appointments'
    ).fetchall()

    conn.close()

    return render_template(
        'admin.html',
        appointments=appointments
    )


# APPROVE APPOINTMENT

@app.route('/approve/<int:id>')
def approve(id):

    if 'admin' not in session:

        return redirect('/login')

    conn = connect_db()

    conn.execute(
        "UPDATE appointments SET status='Approved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')


# DELETE APPOINTMENT

@app.route('/delete/<int:id>')
def delete(id):

    if 'admin' not in session:

        return redirect('/login')

    conn = connect_db()

    conn.execute(
        "DELETE FROM appointments WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')


# AI CHATBOT

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():

    response = ''

    if request.method == 'POST':

        user_message = request.form['message']

        response = get_bot_response(user_message)

    return render_template(
        'chatbot.html',
        response=response
    )


# RUN APPLICATION

if __name__ == '__main__':
    app.run(debug=True)