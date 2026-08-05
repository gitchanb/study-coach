from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
def signup(name,email,password):
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    
    hashed = generate_password_hash(password)
    
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed))
        con.commit()
        con.close()
        return True
    
    except:
        con.close()
        return False
        
    con.close()

#adding a login function

def login(email, password):
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    
    con.close()
    
    if result is None:
        return False
    return check_password_hash(result[0], password)