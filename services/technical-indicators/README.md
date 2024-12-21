# Technical indicators service

Ingest candles from the Kafka topic and generates technical indicators using the ta-lib library and outputs them to a new Kafka topic.

## How to run this code

### 1. Set configuration parameters in the `.env` file
Once Redpanda, Trades and Candles service is up and running, fill in the configuration parameters in the `.env` file.

### 2. Run it
You can run the service using `uv`
```bash
uv run python run.py
```
or
```bash
make run-dev
```
or on docker
```bash
make run
```