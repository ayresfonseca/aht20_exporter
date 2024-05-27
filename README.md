# AHT20 Prometheus Exporter

Python script to read values from AHT20 sensors connected to Raspberry Pi 3B/3B+/4B
and expose metrics over HTTP to be read by Prometheus.

Based on the official [Python client](https://github.com/prometheus/client_python) for Prometheus, [Adafruit CircuitPython AHTx0](https://github.com/adafruit/Adafruit_CircuitPython_AHTx0) and [Adafruit CircuitPython TCA9548A - I2C Multiplexer](https://github.com/adafruit/Adafruit_CircuitPython_TCA9548A) libraries.
