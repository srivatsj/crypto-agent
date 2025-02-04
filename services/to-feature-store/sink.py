from datetime import datetime, timezone

import hopsworks
import pandas as pd
from loguru import logger
from quixstreams.sinks.base import BatchingSink, SinkBackpressureError, SinkBatch


class HopsworksFeatureStoreSink(BatchingSink):
    """
    Some sink writing data to a database
    """

    def __init__(
        self,
        api_key: str,
        project_name: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_group_primary_keys: list[str],
        feature_group_event_time: str,
        feature_group_materialization_minutes: int,
    ):
        """
        Establishes a connection to the Hopsworks feature store.
        """
        super().__init__()
        # Establish a connection to the Hopsworks feature store.
        project = hopsworks.login(api_key_value=api_key, project=project_name)
        self._fs = project.get_feature_store()

        # Get or create the feature group.
        self._feature_group = self._fs.get_or_create_feature_group(
            name=feature_group_name,
            version=feature_group_version,
            primary_key=feature_group_primary_keys,
            event_time=feature_group_event_time,
            online_enabled=True,
        )

        try:
            self._feature_group.materialization_job.schedule(
                cron_expression=f'0 0/{feature_group_materialization_minutes} * ? * *',
                start_time=datetime.now(tz=timezone.utc),
            )
        except Exception as err:
            logger.error(f'Failed to schedule materialization job: {err}')

    def write(self, batch: SinkBatch):
        # Transform the batch into a pandas DataFrame
        data = [item.value for item in batch]
        data = pd.DataFrame(data)

        try:
            # Try to write data to the db
            self._feature_group.insert(data)
        except TimeoutError as err:
            # In case of timeout, tell the app to wait for 30s
            # and retry the writing later
            raise SinkBackpressureError(
                retry_after=30.0,
                topic=batch.topic,
                partition=batch.partition,
            ) from err
