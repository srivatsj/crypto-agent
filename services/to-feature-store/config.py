from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='settings.env', env_file_encoding='utf-8'
    )
    kafka_broker_address: str
    kafka_input_topic: str
    kafka_consumer_group: str
    feature_group_name: str
    feature_group_version: str
    feature_group_primary_keys: list[str]
    feature_group_event_time: str
    data_source: Literal['live', 'historical', 'test']
    feature_group_materialization_minutes: Optional[int] = 15


class HopsworksCredentials(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='credentials.env', env_file_encoding='utf-8'
    )
    hopsworks_api_key: str
    hopsworks_project_name: str


config = Config()
hopsworks_credentials = HopsworksCredentials()
