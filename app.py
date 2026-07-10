import os
import mysql.connector
from flask import Flask, render_template_string
import sys

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Users Database</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; max-width: 1000px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #0078D4; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #f1f1f1; }
    </style>
</head>
<body>
    <h2>Users Directory</h2>
    <table>
        <tr>
            <th>UserID</th>
            <th>Name</th>
            <th>Age</th>
            <th>Phone Number</th>
            <th>Address</th>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ user.UserID }}</td>
            <td>{{ user.Name }}</td>
            <td>{{ user.Age }}</td>
            <td>{{ user.PhoneNumber }}</td>
            <td>{{ user.Address }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def get_db_connection():
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template_string(HTML_TEMPLATE, users=users)
    except Exception as e:
        return f"<h3>Database Connection Failed:</h3><p>{str(e)}</p>", 500

@app.route("/health")
def health_check():
    return {"status": "healthy", "version": sys.version}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
