# Redpanda management
start-redpanda:
	docker compose -f redpanda.yaml up -d

stop-redpanda:
	docker compose -f redpanda.yaml down

add-one-partition-to-trades-topic:
	docker compose -f redpanda.yaml exec redpanda-0 rpk topic add-partitions trades --num 1


# Technical indicators live pipeline
build-technical-indicators-live-pipeline:
	docker compose -f technical-indicators-live-pipeline.yaml build

start-technical-indicators-live-pipeline: build-technical-indicators-live-pipeline
	docker compose -f technical-indicators-live-pipeline.yaml up -d

stop-technical-indicators-live-pipeline:
	docker compose -f technical-indicators-live-pipeline.yaml down


# Technical indicators historical pipeline
build-technical-indicators-historical-pipeline:
	$(eval RUN_ID := $(shell uuidgen))
	echo "RUN_ID: $(RUN_ID)"
	RUN_ID=$$(uuidgen) docker compose -f technical-indicators-historical-pipeline.yaml build

start-technical-indicators-historical-pipeline: build-technical-indicators-historical-pipeline
	docker compose -f technical-indicators-historical-pipeline.yaml up -d

stop-technical-indicators-historical-pipeline:
	docker compose -f technical-indicators-historical-pipeline.yaml down


# News signal live pipeline
build-news-signal-live-pipeline:
	docker compose -f news-signal-live-pipeline.yaml build

start-news-signal-live-pipeline: build-news-signal-live-pipeline
	docker compose -f news-signal-live-pipeline.yaml up -d

stop-news-signal-live-pipeline:
	docker compose -f news-signal-live-pipeline.yaml down

########################################
## Clean up
########################################

# Remove unused Kafka topic after backfill operations
clean-backfill-kakfa-topics:
	@echo "Removing all Kafka topics that contain the word historical"
	docker compose -f redpanda.yaml exec redpanda-0 rpk topic delete -r ".*historical.*"
