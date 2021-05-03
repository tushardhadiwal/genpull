# // Copyright (c) Microsoft Corporation.
# // Licensed under the MIT license.
import logging
import time
import sys
import os
import urllib3
import requests
import json
import json_log_formatter
from influxdb import InfluxDBClient
from datetime import datetime
from utils.flattener import flattening

API_URL = os.getenv("API_URL", "http://localhost:80/api/").split(
    ","
)  # Comma separated list of nifi cluster api urls in case of multiple clusters.
ENDPOINT_LIST = os.getenv(
    "ENDPOINT_LIST",
    "",
).split(",")
MODE = os.getenv(
    "MODE", "unlimited"
)  # In limited mode, only NUMBEROFITERATIONS API calls are made before exiting.
NUMBER_OF_ITERATIONS = int(os.getenv("NUMBER_OF_ITERATIONS", 2))
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", 300))

INFLUXDB_SERVER = os.getenv(
    "INFLUXDB_SERVER", "127.0.0.1"
)  # IP or hostname to InfluxDB server
INFLUXDB_PORT = int(os.getenv("INFLUXDB_PORT", 8086))  # Port on InfluxDB server
INFLUXDB_USERNAME = os.getenv("INFLUXDB_USERNAME", "root")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD", "root")
INFLUXDB_DATABASE = os.getenv("INFLUXDB_DATABASE", "mydb")

count = 0
urllib3.disable_warnings()
conditions = {
    "limited": lambda: count < NUMBER_OF_ITERATIONS,
    "unlimited": lambda: True,
}

# Sysout Logging Setup
logger = logging.getLogger("genpull")
logger.setLevel(logging.INFO)
syshandler = logging.StreamHandler(sys.stdout)
syshandler.setLevel(logging.INFO)
formatter = json_log_formatter.JSONFormatter()
syshandler.setFormatter(formatter)
logger.addHandler(syshandler)


iclient = InfluxDBClient(
    INFLUXDB_SERVER,
    INFLUXDB_PORT,
    INFLUXDB_USERNAME,
    INFLUXDB_PASSWORD,
    INFLUXDB_DATABASE,
)
iclient.create_database(INFLUXDB_DATABASE)


while conditions[MODE]():
    try:
        for AURL in API_URL:
            for ENDPOINT in ENDPOINT_LIST:
                r = (
                    requests.get(url=AURL + ENDPOINT)
                )
                received_response = r.json()
                flat_response = flattening(received_response, "", [])
                current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                points = [
                    {
                        "measurement": ENDPOINT,
                        "tags": {"APIURL": AURL},
                        "time": current_time,
                        "fields": flat_response,
                    }
                ]
                logger.info(ENDPOINT, extra=received_response)
                iclient.write_points(points)
            count += 1
    except Exception as e:
        # this will send an exception to the Application Insights Logs
        logging.exception("Code ran into an unforseen exception!", sys.exc_info()[0])

    time.sleep(SLEEP_INTERVAL)

# logging shutdown will cause a flush of all un-sent telemetry items
logging.shutdown()
