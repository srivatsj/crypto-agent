# To-Feature-Store service

Ingest technical indicators from the Kafka topic and stores them to hopsworks feature store.

## How to run this code

### 1. Set configuration parameters in the `.env` file
Once Redpanda, Trades, Candles and Technical Indicators service is up and running, fill in the configuration parameters in the `.env` file.

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