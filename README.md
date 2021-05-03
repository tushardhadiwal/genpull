# genpull

GenPull is a general purpose container, which allows us to pull JSON data from any HTTP API and store the results in InfluxDB.
This converts a stateless HTTP Response into Stateful Data stored in an InfluxDB which can be queried using Grafana/Chronograf to get historical changes.

```sh
docker run \
--name=genpull \
--network=host -d \
-e INFLUXDB_SERVER="influxdb-grafana" \
-e ENDPOINT_LIST="Endpoint1,Endpoint2,Endpoint3" \
-e SLEEP_INTERVAL=300 \
-e API_URL='http://localhost:80/api' \
--restart unless-stopped \
dtushar/genpull:latest
```
