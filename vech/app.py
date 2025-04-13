from flask import Flask, render_template, request, redirect, url_for, session, flash 
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Initialize the database
def init_db():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                animal TEXT NOT NULL,      
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mechanics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                address TEXT NOT NULL,
                skill TEXT NOT NULL,
                mobile TEXT NOT NULL UNIQUE,
                animal TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
    print("Database initialized.")

init_db()



# Home route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/About')
def About():
    return render_template('About.html')

@app.route('/mechanic')
def mechanic():
    return render_template('mechanic.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/a_dashboard')
def a_dashboard():
    return render_template('a_dashboard.html')

@app.route('/mecreg')
def mecreg():
    return render_template('mecreg.html')

@app.route('/meclogin')
def meclogin():
    return render_template('meclogin.html')


@app.route('/customer_dashboard')
def c_dashboard():
    return render_template('c_dashboard.html') 

@app.route('/c_reset')
def c_reset():
    return render_template('c_reset.html') 



#mechanic registration
@app.route('/mechanic_register', methods=['POST'])
def mechanic_register():
    fname = request.form['fname']
    lname = request.form['lname']
    address = request.form['address']
    skill = request.form['skill']
    mobile = request.form['mobile']
    animal= request.form['animal']
    password = request.form['password']

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO mechanics (fname, lname, address, skill, mobile,animal,password) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (fname, lname, address, skill, mobile,animal,password))
            conn.commit()
            flash('Mechanic registration successful!', 'success')
            return redirect(url_for('meclogin'))
        except sqlite3.IntegrityError:
            flash('Mobile number already registered.', 'error')
            return redirect(url_for('mecreg'))  

#mechanic login
@app.route('/mechanic_login', methods=['POST'])
def mechanic_login():
    mobile = request.form['mobile']
    password = request.form['password']

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mechanics WHERE mobile = ? AND password = ?", (mobile, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['user_mobile'] = user[3]
            flash('Login successful!', 'success')
            return f"Welcome, {user[1]} {user[2]}!"
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('meclogin'))




# customer Registration route
@app.route('/register', methods=['POST'])
def register():
    fname = request.form['fname']
    lname = request.form['lname']
    animal= request.form['animal']
    email = request.form['email']
    password = request.form['password']

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (fname, lname, animal, email, password) VALUES (?, ?, ?, ?, ?)",
                           (fname, lname,animal,email, password))
            conn.commit()
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('customer'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Please log in.', 'error')
            
   

#customer Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['user_email'] = user[3]
            flash('Login successful!', 'success')
            return redirect(url_for('c_dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('customer'))
#customer reset
@app.route('/reset', methods=['POST'])
def reset():
    email = request.form.get('email')
    animal = request.form.get('animal')

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND animal = ?", (email, animal))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['user_email'] = user[3]
            return redirect(url_for('cpass_up'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('customer'))  

     
#customer pass change
@app.route('/cpass_up')
def cpass_up():
    new_password = request.form.get('password')
    email=request.form.get('email')

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users  SET password = ? WHERE email= ? ", (new_password, email))
        user = cursor.fetchone()

        if user:
            flash('Password successful changed')
            return redirect(url_for('customer'))
# Logout
@app.route('/logout')
def logout():
    session.clear()
    
    return redirect(url_for('customer'))

@app.route('/back')
def back():
    session.clear()
    
    return redirect(url_for('mechanic'))
if __name__ == '__main__':
    app.run(debug=True)
