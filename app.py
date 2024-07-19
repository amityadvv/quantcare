from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donors
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, blood_type TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    blood_type = request.form['blood_type']
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO donors (name, email, phone, blood_type) VALUES (?, ?, ?, ?)",
              (name, email, phone, blood_type))
    conn.commit()
    conn.close()
    
    send_email(name, email, phone, blood_type)
    
    return redirect(url_for('index'))

def send_email(name, email, phone, blood_type):
    sender_email = "your-email@gmail.com"
    receiver_email = "2k23.cs2314011@gmail.com"
    password = "your-email-password"
    
    message = MIMEMultipart()
    message["Subject"] = "New Blood Donation Registration"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nBlood Type: {blood_type}"
    message.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
