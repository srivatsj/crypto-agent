run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t candles .

run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		candles

build-multistage:
	docker build -f multistage.Dockerfile -t candles:multistage .

run-multistage: build-multistage
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		candles:multistage


build-all: build build-multistage