from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='openai_credentials.env', env_file_encoding='utf-8'
    )
    model_name: str
    api_key: str


openai_config = OpenAIConfig()
