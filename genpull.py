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

# count = 0
urllib3.disable_warnings()
# conditions = {
#     "limited": lambda: count < NUMBER_OF_ITERATIONS,
#     "unlimited": lambda: True,
# }

# Sysout Logging Setup
logger = logging.getLogger("genpull")
logger.setLevel(logging.INFO)
syshandler = logging.StreamHandler(sys.stdout)
syshandler.setLevel(logging.INFO)
formatter = json_log_formatter.JSONFormatter()
syshandler.setFormatter(formatter)
logger.addHandler(syshandler)


# iclient = InfluxDBClient(
#     INFLUXDB_SERVER,
#     INFLUXDB_PORT,
#     INFLUXDB_USERNAME,
#     INFLUXDB_PASSWORD,
#     INFLUXDB_DATABASE,
# )
# iclient.create_database(INFLUXDB_DATABASE)
config ={}

while True:
    with open("config.json", "r") as f:
        latest_config = json.load(f)
    
    if latest_config != config:
        config=latest_config
        API_URL = config["API_URL"].split(",")  # Comma separated list of api urls in case of multiple apis.
        ENDPOINT_LIST = config["ENDPOINT_LIST"].split(",")
        # MODE = config["MODE"]  # In limited mode, only NUMBEROFITERATIONS API calls are made before exiting.
        # NUMBER_OF_ITERATIONS = int(config["NUMBER_OF_ITERATIONS"])
        SLEEP_INTERVAL = int(config["SLEEP_INTERVAL"])

        INFLUXDB_SERVER = config["INFLUXDB_SERVER"]  # IP or hostname to InfluxDB server
        INFLUXDB_PORT = int(config["INFLUXDB_PORT"])  # Port on InfluxDB server
        INFLUXDB_USERNAME = config["INFLUXDB_USERNAME"]
        INFLUXDB_PASSWORD = config["INFLUXDB_PASSWORD"]
        INFLUXDB_DATABASE = config["INFLUXDB_DATABASE"]
        iclient = InfluxDBClient(INFLUXDB_SERVER,INFLUXDB_PORT,INFLUXDB_USERNAME,INFLUXDB_PASSWORD,INFLUXDB_DATABASE,)
        iclient.create_database(INFLUXDB_DATABASE)
        # conditions = {
        # "limited": lambda: count < NUMBER_OF_ITERATIONS,
        # "unlimited": lambda: True,
        # }
        count = 0
        if config['STOP'] != "False":
            logger.info("STOP Request Received, Exiting")
            break

    # while conditions[MODE]():
    try:
        for AURL in API_URL:
            for ENDPOINT in ENDPOINT_LIST:
                r = requests.get(url=AURL + ENDPOINT)
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
