from flask import Flask
import sys

app = Flask(__name__)

@app.route("/")
def home():
    python_version = sys.version
    return f"Hello from Azure Web Apps! Running on Python version: {python_version}"

@app.route("/health")
def health_check():
    return {"status": "healthy", "version": sys.version}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
