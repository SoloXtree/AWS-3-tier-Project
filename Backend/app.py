from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import time

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
CORS(app)

# -----------------------------
# Prometheus Metrics
# -----------------------------

REQUEST_COUNT = Counter(
    'flask_requests_total',
    'Total number of requests'
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'Request latency in seconds'
)

# -----------------------------
# Database configuration
# -----------------------------

db_config = {
    "host": "vky.czwou6k42ebc.eu-west-2.rds.amazonaws.com",
    "user": "admin",
    "password": "15406578",
    "database": "vky1"
}

# -----------------------------
# Health Check
# -----------------------------

@app.route('/')
def health_check():
    REQUEST_COUNT.inc()
    return jsonify({"status": "Backend is running!"}), 200


# -----------------------------
# Login Endpoint
# -----------------------------

@app.route('/login')
def login():

    start_time = time.time()
    REQUEST_COUNT.inc()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT username, email FROM users LIMIT 1;")
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        REQUEST_LATENCY.observe(time.time() - start_time)

        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "No users found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Users Endpoint
# -----------------------------

@app.route('/users')
def get_users():

    start_time = time.time()
    REQUEST_COUNT.inc()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT username, email FROM users;")
        users = cursor.fetchall()

        cursor.close()
        conn.close()

        REQUEST_LATENCY.observe(time.time() - start_time)

        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Prometheus Metrics Endpoint
# -----------------------------

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# -----------------------------
# Run Flask App
# -----------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
