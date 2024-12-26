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
    polling_interval_seconds: int


cryptopanic_config = CryptopanicConfig()
config = Config()
