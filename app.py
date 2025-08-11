from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from flask import session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messaging and sessions

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone=? AND password=?", (phone, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = phone
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Or wherever your home page is
        else:
            flash('Invalid phone number or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    phone = session['user']
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, plan FROM users WHERE phone=?", (phone,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template('dashboard.html', name=user[0], phone=user[1], plan=user[2])
    else:
        flash('User not found', 'danger')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))


import sqlite3

@app.route('/summit', methods=['POST'])
def summit():
    name = request.form['name']
    phone = request.form['phone']
    password = request.form['password']
    plan = request.form['plan']
    file = request.files['payment_proof']

    filename = ""
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

    try:
        with sqlite3.connect('database.db', timeout=10) as conn:
            cursor = conn.cursor()

            # Check if phone number already exists
            cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
            existing_user = cursor.fetchone()

            if existing_user:
                error = "This phone number is already registered."
                return render_template("register.html", error=error)

            # Insert into database
            cursor.execute(
                "INSERT INTO users (name, phone, password, plan, payment_proof) VALUES (?, ?, ?, ?, ?)",
                (name, phone, password, plan, filename)
            )
            conn.commit()

    except sqlite3.OperationalError as e:
        error = f"Database error: {str(e)}"
        return render_template("register.html", error=error)

    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run(debug=True)
