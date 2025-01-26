from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class CryptopanicConfig(BaseSettings):
    """
    Configuration for the Cryptopanic API
    """

    model_config = SettingsConfigDict(
        env_file='cryptopanic_credentials.env', env_file_encoding='utf-8'
    )
    api_key: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='settings.env', env_file_encoding='utf-8'
    )
    kafka_broker_address: str
    kafka_output_topic: str
    data_source: Literal['live', 'historical']
    polling_interval_seconds: Optional[int] = 10
    historical_data_source_url: Optional[str] = None


cryptopanic_config = CryptopanicConfig()
config = Config()
