"""
This script reads temperature and humidity data from multiple AHTx0 sensors
connected via a TCA9548A I2C multiplexer and exposes the data as Prometheus metrics.
"""

import time
import board
import adafruit_tca9548a
import adafruit_ahtx0
from prometheus_client import start_http_server, Gauge

# Constants
SLEEP_INTERVAL = 2.0
HTTP_SERVER_PORT = 9101

# Prometheus metrics
aht20_temperature_celsius = Gauge(
    "aht20_temperature_celsius",
    "Temperature in celsius provided by aht sensor",
    ["sensor"],
)
aht20_humidity = Gauge(
    "aht20_humidity", "Humidity in percents provided by dht sensor", ["sensor"]
)


def read_sensor(sensor, label):
    """
    Reads temperature and humidity from the given sensor and updates the Prometheus metrics.

    Args:
        sensor: The sensor object to read data from.
        label: The label for the Prometheus metrics.
    """
    try:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        aht20_humidity.labels(label).set(f"{humidity:.1f}")
        aht20_temperature_celsius.labels(label).set(f"{temperature:.1f}")
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])


def main():
    """
    Main function to initialize sensors and start the Prometheus HTTP server.
    """
    # Start up the server to expose the metrics.
    start_http_server(HTTP_SERVER_PORT)

    # Create I2C bus as normal
    i2c = board.I2C()

    # Create the TCA9548A object and give it the I2C bus
    tca = adafruit_tca9548a.TCA9548A(i2c)

    # Create sensor objects, communicating over the board's default I2C bus
    sensors = [
        (adafruit_ahtx0.AHTx0(tca[0]), "sensor0"),
        (adafruit_ahtx0.AHTx0(tca[1]), "sensor1"),
        (adafruit_ahtx0.AHTx0(tca[2]), "sensor2"),
    ]

    while True:
        for aht, prom_label in sensors:
            read_sensor(aht, prom_label)
        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main()
