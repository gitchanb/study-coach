from flask import Flask, render_template,request,redirect, url_for, session
from auth import signup, login
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq
import os
from dotenv import load_dotenv
import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

init_db()

load_dotenv()

app = Flask(__name__)
app.secret_key = 'auqkjdhfakjsh'
api_key =os.getenv ('GROQ_API_KEY')
client = Groq(api_key=api_key)

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        signup(name, email, password)
        return redirect(url_for('login_page'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if login(email, password):
            session['user'] = email
            return redirect(url_for('home'))
        return render_template('login.html', error='Wrong password or email!') 
    return render_template('login.html')

@app.route('/',methods=['GET','POST'])
def home():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    result = None
    if request.method == 'POST':
        topic = request.form['topic']
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert study coach. When given a topic, create a structured study plan with key concepts, resources, and daily schedule. Be specific and practical also at end concisely use 80/20 rule,prerequisite,metalearning ideas."},
                {"role": "user", "content": topic}
            ]
        )
        return render_template('index.html', response=response.choices[0].message.content)
    return render_template('index.html', response=None)
if __name__ == '__main__':
    app.run(debug=True)
