start-redpanda:
	docker compose -f redpanda.yaml up -d

stop-redpanda:
	docker compose -f redpanda.yaml down

add-one-partition-to-trades-topic:
	docker compose -f redpanda.yaml exec redpanda-0 rpk topic add-partitions trades --num 1
