run-dev-live:
	cp live.settings.env settings.env
	uv run python run.py

run-dev-historical:
	cp historical.settings.env settings.env
	uv run python run.py

build:
	docker build -f Dockerfile -t trades .

run: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		trades