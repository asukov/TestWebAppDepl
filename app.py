from flask import Flask, jsonify
import mysql.connector
import os
import sys

app = Flask(__name__)

def get_db_connection():
    # It is highly recommended to store the password in Azure App Settings
    # rather than hardcoding it in your repository.
    db_password = os.environ.get("DB_PASSWORD", "YOUR_DEFAULT_PASSWORD_HERE")
    
    return mysql.connector.connect(
        host="10.0.0.4",
        port=3306,
        user="asukov",
        password=db_password,
        database="users"
    )

@app.route("/")
def home():
    return "Hello from Azure! Navigate to /users to see the database records."

@app.route("/users")
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health_check():
    return {"status": "healthy", "version": sys.version}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
