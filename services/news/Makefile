run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t news .

run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		news