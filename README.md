# genpull

GenPull is a general purpose container, which allows us to pull JSON data from any HTTP API and store the results in InfluxDB.
This converts a stateless HTTP Response into Stateful Data stored in an InfluxDB which can be queried using Grafana/Chronograf to get historical changes.

Please create a file `config.json` and set parameters as per requirement.
```
{
{
	"API_LIST": [
        {
			"API_URL": "https://api.countapi.xyz/hit/",
			"ENDPOINT_LIST": "microsoft.com,monitofi.com",
			"SINK": "InfluxDB1",
			"AUTH_TYPE": "None",
			"USERNAME": "",
			"PASSWORD": ""
		},
		{
			"API_URL": "https://api.countapi.xyz/",
			"ENDPOINT_LIST": "hit/test1.com,hit/test2.com",
			"SINK": "InfluxDB2",
			"AUTH_TYPE": "HTTPBasicAuth",
			"USERNAME": "testuser",
			"PASSWORD": "replaceme"
		}
	],

	"SINKS": [
	  {
			"NAME": "InfluxDB1",
			"INFLUXDB_SERVER": "8.8.8.80",
			"INFLUXDB_PORT": 8086,
			"INFLUXDB_USERNAME": "root",
			"INFLUXDB_PASSWORD": "root",
			"INFLUXDB_DATABASE": "testdb2"

		},
		{
			"NAME": "InfluxDB2",
			"INFLUXDB_SERVER": "55.11.11.11",
			"INFLUXDB_PORT": 8086,
			"INFLUXDB_USERNAME": "root",
			"INFLUXDB_PASSWORD": "root",
			"INFLUXDB_DATABASE": "testdb1"
		}
	],

	"STOP": "False",
    "SLEEP_INTERVAL": 120
}
}
```

# Quick Start

```sh
docker run \
--name=genpull \
--network=host -d \
-v $(pwd)/config.json:/opt/genpull/config.json \
--restart unless-stopped \
dtushar/genpull:latest
```

Added GenPull 2.0 Features: 
Separate object per API
Support for Basic and Digest HTTP Auth
Many to Many Source Sink Mapping