from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this!

CSV_FILE = 'users.csv'

# Ensure CSV exists with headers
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            f.write("username,email,password\n")

def read_users():
    users = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users.append(row)
    return users

def write_user(user):
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user['username'], user['email'], user['password']])

@app.route('/', methods=['GET', 'POST'])
def index():
    init_csv()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'signup':
            username = request.form['username'].strip()
            email = request.form['email'].strip()
            password = request.form['password'].strip()

            if not username or not email or not password:
                flash('Please fill all signup fields')
                return redirect(url_for('index'))

            users = read_users()
            for user in users:
                if user['username'] == username:
                    flash('Username already exists')
                    return redirect(url_for('index'))
                if user['email'] == email:
                    flash('Email already registered')
                    return redirect(url_for('index'))

            write_user({'username': username, 'email': email, 'password': password})
            flash('Signup successful! Please login.')
            return redirect(url_for('index'))

        elif action == 'login':
            username = request.form['username'].strip()
            password = request.form['password'].strip()

            users = read_users()
            for user in users:
                if user['username'] == username and user['password'] == password:
                    session['username'] = username
                    flash('Login successful!')
                    return redirect(url_for('home'))

            flash('Invalid username or password')
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/home')
def home():
    if 'username' not in session:
        flash('Please login first')
        return redirect(url_for('index'))
    return f"<h1>Welcome {session['username']}!</h1><a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
