# AHT20 Prometheus Exporter

Python script to read values from AHTx0 sensors (AHT20) connected to a Raspberry Pi (3B/3B+/4B) via a TCA9548A I2C multiplexer and expose temperature and humidity metrics over HTTP for Prometheus.

Based on the official [Python client](https://github.com/prometheus/client_python) for Prometheus, [Adafruit CircuitPython AHTx0](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0) and [Adafruit CircuitPython TCA9548A - I2C Multiplexer](https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A) libraries.

## Features

- Reads temperature and humidity from multiple AHTx0 sensors via TCA9548A multiplexer
- Exposes metrics in Prometheus format
- Per-sensor availability metric (`aht20_sensor_up`) for alerting
- Flexible sensor count and HTTP port via CLI arguments or environment variables
- Graceful shutdown on `SIGTERM`/`SIGINT`

## Requirements

- Python >= 3.11
- Poetry >= 2.0
- Raspberry Pi or compatible board with I2C enabled
- AHTx0 sensors connected via TCA9548A multiplexer

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/ayresfonseca/aht20_exporter.git
   cd aht20_exporter
   ```

2. Install dependencies with Poetry:
   ```sh
   poetry install
   ```

## Usage

Run the exporter (default: 3 sensors):
```sh
poetry run aht20_exporter
```

Specify the number of sensors:
```sh
poetry run aht20_exporter --sensors 4
```

Override the HTTP port:
```sh
poetry run aht20_exporter --port 9200
```

All options are also configurable via environment variables:
```sh
export AHT20_SENSOR_COUNT=4
export AHT20_PORT=9200
poetry run aht20_exporter
```

Metrics will be available at [http://localhost:9101/metrics](http://localhost:9101/metrics) (or your chosen port).

## Prometheus Metrics

| Metric | Description |
|--------|-------------|
| `aht20_temperature_celsius{sensor="sensorN"}` | Temperature in Celsius |
| `aht20_humidity{sensor="sensorN"}` | Relative humidity in percent |
| `aht20_sensor_up{sensor="sensorN"}` | `1` if the sensor is reachable, `0` on error |

Sensors are labeled `sensor0`, `sensor1`, etc. Use `aht20_sensor_up` for alerting on sensor failures.

## Development

```sh
poetry run black .                                          # format
flake8 --extend-ignore=E501 $(git ls-files '*.py')         # style check
pylint --disable=C0301 $(git ls-files '*.py')              # lint
```

> **Note:** `board`, `adafruit_tca9548a`, and `adafruit_ahtx0` require physical I2C hardware. The exporter cannot be tested without a Raspberry Pi with AHT20 sensors attached.

## Troubleshooting

- Ensure I2C is enabled on your Raspberry Pi.
- Check sensor wiring and addresses.
- Review logs for initialization errors.

## License

MIT License

---
