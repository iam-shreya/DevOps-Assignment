"""Demo web app instrumented with Prometheus metrics (prometheus_client)."""
import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from prometheus_client import Counter, Gauge, Histogram, start_http_server

REQUESTS = Counter("app_requests_total", "Total HTTP requests", ["endpoint", "status"])
LATENCY = Histogram("app_request_duration_seconds", "Request latency in seconds", ["endpoint"],
                    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0))
IN_PROGRESS = Gauge("app_requests_in_progress", "Requests currently being processed")
ORDERS = Counter("app_orders_total", "Business metric: orders placed")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        endpoint = self.path.split("?")[0]
        IN_PROGRESS.inc()
        start = time.time()
        if endpoint == "/order":
            time.sleep(random.uniform(0.05, 0.3))
            status = 500 if random.random() < 0.1 else 200
            if status == 200:
                ORDERS.inc()
        elif endpoint == "/":
            time.sleep(random.uniform(0.005, 0.05))
            status = 200
        else:
            status = 404
        LATENCY.labels(endpoint).observe(time.time() - start)
        REQUESTS.labels(endpoint, str(status)).inc()
        IN_PROGRESS.dec()
        body = f"status={status}\n".encode()
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    start_http_server(8001)          # /metrics endpoint for Prometheus
    print("App on :8000, metrics on :8001/metrics", flush=True)
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
