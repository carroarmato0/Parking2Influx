#!/usr/bin/python3

# Import modules
import docker
import json
import requests

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

    # Loop through data
    for parking in data['records']:
        payload.append(
            "{measurement},city={city},name={name},description={description},latitude={latitude},longitude={longitude} "
            "max_capacity={max_capacity},current_capacity={current_capacity},open={is_open}".format(
                measurement="state",
                name=parking["fields"]["name"].replace(" ", "\\ "),
                city=json.loads(parking["fields"]["city"])['name'],
                description=parking["fields"]["description"].replace(" ", "\\ "),
                latitude=parking["fields"]["latitude"],
                longitude=parking["fields"]["longitude"],
                max_capacity=json.loads(parking["fields"]["parkingstatus"])["totalCapacity"],
                current_capacity=json.loads(parking["fields"]["parkingstatus"])["availableCapacity"],
                is_open=int(json.loads(parking["fields"]["parkingstatus"])["open"] == True)
            )
        )

    client.write_points(payload, batch_size=len(payload), protocol='line')


def resolve_container_address(container):
    client = docker.from_env()
    container = client.containers.get(container)
    container_networks = container.attrs['NetworkSettings']['Networks']
    container_network_device = next(iter(container_networks.keys()))

    return container_networks[container_network_device]['IPAddress']


def main():
    influx_ip = resolve_container_address("influxdb")
    parking_data = fetch_parking("https://data.stad.gent/api/records/1.0/search/?dataset=bezetting-parkeergarages"
                                 "-real-time&q=&facet=description")
    submit_data(influx_ip, "parking", parking_data)


if __name__ == "__main__":
    main()
