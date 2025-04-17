from flask import Flask, request
import requests
import time
from google.cloud import bigquery
from datetime import datetime

app = Flask(__name__)
bq = bigquery.Client()
table_id = "websiteuptime.uptime_monitoring.website_logs"

@app.route("/", methods=["GET"])
def check_websites():
    websites = ["https://facebook.com", "https://youtube.com", "https://www.instagram.com", "https://gvsu.edu", "https://open.spotify.com"]
    for url in websites:
        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            elapsed = time.time() - start
            status = response.status_code
            success = status == 200
        except Exception:
            elapsed = 0
            status = 0
            success = False

        row = [{
            "timestamp": datetime.utcnow().isoformat(),
            "url": url,
            "status_code": status,
            "response_time": elapsed,
            "success": success
        }]
        bq.insert_rows_json(table_id, row)

    return "Uptime check complete", 200
