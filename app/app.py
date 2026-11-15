from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Counts HTTP requests by endpoint
REQUEST_COUNT = Counter(
    "sre_http_requests_total",
    "Total number of HTTP requests",
    ["endpoint"]
)

# Counts simulated application errors
ERROR_COUNT = Counter(
    "sre_http_errors_total",
    "Total number of HTTP errors"
)

# Measures request latency
REQUEST_LATENCY = Histogram(
    "sre_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"]
)


@app.route("/")
def home():
    start_time = time.time()

    REQUEST_COUNT.labels(endpoint="/").inc()

    response = jsonify({
        "message": "SRE Final Project API",
        "status": "running"
    })

    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start_time)

    return response


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()

    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/simulate-error")
def simulate_error():
    REQUEST_COUNT.labels(endpoint="/simulate-error").inc()
    ERROR_COUNT.inc()

    return jsonify({
        "status": "error",
        "message": "Simulated application error"
    }), 500


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)