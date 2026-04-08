from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_region: str
    bedrock_text_model_id: str
    bedrock_embed_model_id: str

    class Config:
        env_file = ".env"

settings = Settings()