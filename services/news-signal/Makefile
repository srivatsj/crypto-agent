run-openai:
	uv run python -m llms.openai

run-ollama:
	uv run python -m llms.ollama


# To generate golden dataset with instruction input and output tuples
# to fine tune our model
run-golden-dataset-with-openai:
	uv run python golden_dataset.py \
		--model_provider openai \
		--output_file ./data/golden_dataset_openai.json \
		--n 50

run-golden-dataset-with-ollama:
	uv run python golden_dataset.py \
		--model_provider ollama \
		--output_file ./data/golden_dataset_ollama.json \
		--n 50

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