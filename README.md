# genpull

GenPull is a general purpose container, which allows us to pull JSON data from any HTTP API and store the results in InfluxDB.
This converts a stateless HTTP Response into Stateful Data stored in an InfluxDB which can be queried using Grafana/Chronograf to get historical changes.

Please create a file `config.json` and set parameters as per requirement.
```
{
    "API_URL": "http://localhost:80/api/,http://localhost:8081/api2/",
    "ENDPOINT_LIST": "EndPoint1,EndPoint2,Endpoint3",
    "SINK": "InfluxDB?Telegraf?",
    "SLEEP_INTERVAL": 300,
    "INFLUXDB_SERVER": "127.0.0.1",
    "INFLUXDB_PORT": 8086,
    "INFLUXDB_USERNAME": "root",
    "INFLUXDB_PASSWORD": "root",
    "INFLUXDB_DATABASE": "mydb",
    "STOP": "False"
}
```

#Quick Start

```sh
docker run \
--name=genpull \
--network=host -d \
-v $(pwd)/config.json:/opt/genpull/config.json \
--restart unless-stopped \
dtushar/genpull:latest
```