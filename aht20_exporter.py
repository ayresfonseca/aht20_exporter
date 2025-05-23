"""
This script reads temperature and humidity data from multiple AHTx0 sensors
connected via a TCA9548A I2C multiplexer and exposes the data as Prometheus metrics.
"""

import time
import os
import logging
import argparse
import board
import adafruit_tca9548a
import adafruit_ahtx0
from prometheus_client import start_http_server, Gauge

# Constants
SLEEP_INTERVAL = 2.0  # Time to wait between sensor readings (in seconds)
HTTP_SERVER_PORT = 9101  # Port for Prometheus metrics server

# Prometheus metrics
aht20_temperature_celsius = Gauge(
    "aht20_temperature_celsius",
    "Temperature in Celsius provided by AHT sensor",
    ["sensor"],
)
aht20_humidity = Gauge(
    "aht20_humidity", "Humidity in percent provided by AHT sensor", ["sensor"]
)

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


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
        # Update Prometheus metrics with formatted values
        aht20_humidity.labels(label).set(float(f"{humidity:.1f}"))
        aht20_temperature_celsius.labels(label).set(float(f"{temperature:.1f}"))
    except RuntimeError as error:
        # Sensor read errors are common, just log and continue
        logging.warning("Sensor %s read error: %s", label, error.args[0])
    except Exception as e:  # pylint: disable=broad-except
        # Log any unexpected errors
        logging.error("Unexpected error on sensor %s: %s", label, e)


def main():
    """
    Main function to initialize sensors and start the Prometheus HTTP server.
    """
    parser = argparse.ArgumentParser(description="AHT20 Prometheus exporter")
    parser.add_argument(
        "--sensors",
        type=int,
        default=int(os.getenv("AHT20_SENSOR_COUNT", "3")),
        help="Number of AHT20 sensors to use (default: 3)",
    )
    args = parser.parse_args()

    # Start Prometheus HTTP server
    start_http_server(HTTP_SERVER_PORT)
    i2c = board.I2C()
    tca = adafruit_tca9548a.TCA9548A(i2c)

    sensors = []
    for idx in range(args.sensors):
        try:
            # Initialize each sensor and assign a label
            sensors.append((adafruit_ahtx0.AHTx0(tca[idx]), f"sensor{idx}"))
        except Exception as e:  # pylint: disable=broad-except
            logging.warning("Could not initialize sensor %d: %s", idx, e)

    if not sensors:
        logging.error("No sensors initialized, exiting program.")
        return

    # Main loop: read all sensors and update metrics
    while True:
        for aht, prom_label in sensors:
            read_sensor(aht, prom_label)
        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main()
