# // Copyright (c) Microsoft Corporation.
# // Licensed under the MIT license.
import logging
import time
import sys
import os
import urllib3
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import json
import json_log_formatter
from influxdb import InfluxDBClient
from datetime import datetime
from utils.flattener import flattening

urllib3.disable_warnings()

# Sysout Logging Setup
logger = logging.getLogger("genpull")
logger.setLevel(logging.INFO)
syshandler = logging.StreamHandler(sys.stdout)
syshandler.setLevel(logging.INFO)
formatter = json_log_formatter.JSONFormatter()
syshandler.setFormatter(formatter)
logger.addHandler(syshandler)

config ={}
sinks_dict={}

while True:
    with open("config.json", "r") as f:
        latest_config = json.load(f)
    
    if latest_config != config:
        config=latest_config
        #Check if all sinks have a unique name, check if each api is mapped to valid sink?
        for sink in config['SINKS']:
            if sink['TYPE']=="INFLUXDB":
                iclient = InfluxDBClient(sink["INFLUXDB_SERVER"],int(sink["INFLUXDB_PORT"]),sink["INFLUXDB_USERNAME"],sink["INFLUXDB_PASSWORD"],sink["INFLUXDB_DATABASE"],)
                iclient.create_database(sink["INFLUXDB_DATABASE"])
                sinks_dict[sink['NAME']]=iclient
            elif sink['TYPE']=="TELEGRAF":
                sinks_dict[sink['NAME']]=sink['TELEGRAF_URL']

        SLEEP_INTERVAL = int(config["SLEEP_INTERVAL"])
        count = 0
        if config['STOP'] != "False":
            logger.info("STOP Request Received, Exiting")
            break

    try:
        for apiobj in config['API_LIST']:
            if apiobj['SINK_TYPE'] in ["INFLUXDB","TELEGRAF"]:
                #Means its a suuported sink
                ENDPOINT_LIST=apiobj['ENDPOINT_LIST'].split(",")
                for ENDPOINT in ENDPOINT_LIST:

                    if apiobj['AUTH_TYPE']=="HTTPBasicAuth":
                        r = requests.get(url=str(apiobj['API_URL']+ENDPOINT), auth = HTTPBasicAuth(apiobj['USERNAME'], apiobj['PASSWORD']))
                    elif apiobj['AUTH_TYPE']=="HTTPDigestAuth":
                        r = requests.get(url=str(apiobj['API_URL']+ENDPOINT), auth = HTTPDigestAuth(apiobj['USERNAME'], apiobj['PASSWORD']))
                    else :
                        r = requests.get(url=str(apiobj['API_URL']+ENDPOINT))

                    received_response = r.json()
                    if apiobj['SINK_TYPE']=="INFLUXDB":
                        flat_response = flattening(received_response, "", [])
                        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                        points = [
                            {
                                "measurement": ENDPOINT,
                                "tags": {"APIURL": apiobj['API_URL']},
                                "time": current_time,
                                "fields": flat_response,
                            }
                        ]
                        logger.info(apiobj['API_URL']+ENDPOINT, extra=received_response)
                        iclient=sinks_dict[apiobj['SINK_NAME']]
                        iclient.write_points(points)

                    elif apiobj['SINK_TYPE']=="TELEGRAF":
                        requests.post(sinks_dict[apiobj['SINK_NAME']], json=received_response)
                        logger.info(apiobj['API_URL']+ENDPOINT, extra=received_response)

            else:
                print("Error: Please define a Supported Sink Type instead of "+apiobj['SINK_TYPE']+ "in the config.")

        count += 1
    except Exception as e:
        # this will send an exception to the Application Insights Logs
        logging.exception("Code ran into an unforseen exception!", sys.exc_info()[0])

    time.sleep(SLEEP_INTERVAL)

# logging shutdown will cause a flush of all un-sent telemetry items
logging.shutdown()
