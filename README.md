# AHT20 Prometheus Exporter

Python script to read values from AHTx0 sensors (AHT20) connected to a Raspberry Pi (3B/3B+/4B) via a TCA9548A I2C multiplexer and expose temperature and humidity metrics over HTTP for Prometheus.

Based on the official [Python client](https://github.com/prometheus/client_python) for Prometheus, [Adafruit CircuitPython AHTx0](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0) and [Adafruit CircuitPython TCA9548A - I2C Multiplexer](https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A) libraries.

## Features

- Reads temperature and humidity from multiple AHTx0 sensors via TCA9548A multiplexer
- Exposes metrics in Prometheus format
- Flexible sensor count via CLI argument or environment variable

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
Or via environment variable:
```sh
export AHT20_SENSOR_COUNT=4
poetry run aht20_exporter
```

Metrics will be available at [http://localhost:9101/metrics](http://localhost:9101/metrics).

## Prometheus Metrics

- `aht20_temperature_celsius{sensor="sensor0"}`
- `aht20_humidity{sensor="sensor0"}`

Each sensor is labeled as `sensor0`, `sensor1`, etc.

## Development

- Format code: `poetry run black .`
- Lint code: `poetry run pylint aht20_exporter.py`

## Troubleshooting

- Ensure I2C is enabled on your Raspberry Pi.
- Check sensor wiring and addresses.
- Review logs for initialization errors.

## License

MIT License

---
