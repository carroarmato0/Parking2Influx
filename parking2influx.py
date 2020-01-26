#!/usr/bin/python3

# Import modules
import json, requests, docker, time
from influxdb import InfluxDBClient

def fetch_parking(api_url):
    # Fetch Data
    api_descriptor = requests.get(api_url)
    api_data = json.loads(api_descriptor.content)
    api_descriptor.close()
    return api_data

def submit_data(influxdb_ip, database, data):
		client = InfluxDBClient(host=influxdb_ip, port=8086)
		client.switch_database(database)

		payload = []

		timestamp = int(time.time())

		# Loop through data
		for parking in data:
				payload.append(
						"{measurement},city={city},name={name},description={description},latitude={latitude},longitude={longitude} " \
						"max_capacity={max_capacity},current_capacity={current_capacity},open={is_open} {timestamp}" \
						.format(
							measurement="state",
							city=parking["city"]["name"],
							name=parking["name"].replace(" ", "\\ "),
							description=parking["description"].replace(" ", "\\ "),
							latitude=parking["latitude"],
							longitude=parking["longitude"],
							max_capacity=parking["parkingStatus"]["totalCapacity"],
							current_capacity=parking["parkingStatus"]["availableCapacity"],
							is_open=int(parking["parkingStatus"]["open"] == True),
							timestamp=timestamp))

		client.write_points(payload, batch_size=len(payload), protocol='line')

def resolve_container_address(container):
		client = docker.from_env()
		container = client.containers.get(container)
		container_networks = container.attrs['NetworkSettings']['Networks']
		container_network_device = next(iter(container_networks.keys()))

		return container_networks[container_network_device]['IPAddress']

def main():
		influx_ip = resolve_container_address("influxdb")
		parking_data = fetch_parking("https://datatank.stad.gent/4/mobiliteit/bezettingparkingsrealtime.json")
		submit_data(influx_ip, "parking", parking_data)

if __name__ == "__main__":
    main()
