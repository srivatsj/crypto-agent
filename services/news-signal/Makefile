run-openai:
	uv run python -m llms.openai

run-ollama:
	uv run python -m llms.ollama

run-dev:
	uv run python run.py

build:
	docker build -f Dockerfile -t news-signal .

run-with-openai: build
	docker run -it \
		--network redpanda_network \
		-e KAFKA_BROKER_ADDRESS=redpanda-0:9092 \
		-e MODEL_PROVIDER=openai \
		news-signal