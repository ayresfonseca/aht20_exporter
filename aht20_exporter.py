"""
This script reads temperature and humidity data from multiple AHTx0 sensors
connected via a TCA9548A I2C multiplexer and exposes the data as Prometheus metrics.
"""

import os
import signal
import logging
import argparse
import threading
import board
import adafruit_tca9548a
import adafruit_ahtx0
from prometheus_client import start_http_server, Gauge

# Constants
SLEEP_INTERVAL = 2.0  # Time to wait between sensor readings (in seconds)
DEFAULT_HTTP_PORT = 9101  # Default port for Prometheus metrics server

# Prometheus metrics
aht20_temperature_celsius = Gauge(
    "aht20_temperature_celsius",
    "Temperature in Celsius provided by AHT sensor",
    ["sensor"],
)
aht20_humidity = Gauge(
    "aht20_humidity", "Humidity in percent provided by AHT sensor", ["sensor"]
)
aht20_sensor_up = Gauge(
    "aht20_sensor_up", "Whether the AHT sensor is reachable (1=up, 0=down)", ["sensor"]
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
        aht20_humidity.labels(label).set(round(humidity, 1))
        aht20_temperature_celsius.labels(label).set(round(temperature, 1))
        aht20_sensor_up.labels(label).set(1)
    except RuntimeError as error:
        logging.warning("Sensor %s read error: %s", label, error.args[0])
        aht20_sensor_up.labels(label).set(0)
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Unexpected error on sensor %s: %s", label, e)
        aht20_sensor_up.labels(label).set(0)


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
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("AHT20_PORT", str(DEFAULT_HTTP_PORT))),
        help=f"HTTP port for Prometheus metrics (default: {DEFAULT_HTTP_PORT})",
    )
    args = parser.parse_args()

    shutdown_event = threading.Event()

    def handle_signal(signum, frame):  # pylint: disable=unused-argument
        logging.info("Received signal %d, shutting down...", signum)
        shutdown_event.set()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    start_http_server(args.port)
    logging.info("Prometheus metrics available at http://localhost:%d/metrics", args.port)
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

    while not shutdown_event.is_set():
        for aht, prom_label in sensors:
            read_sensor(aht, prom_label)
        shutdown_event.wait(SLEEP_INTERVAL)

    logging.info("Exporter stopped.")


if __name__ == "__main__":
    main()
