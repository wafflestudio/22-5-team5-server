from pydantic_settings import BaseSettings, SettingsConfigDict
from wastory.settings import SETTINGS


class DatabaseSettings(BaseSettings):
    dialect: str = ""
    driver: str = ""
    host: str = ""
    port: int = 0
    user: str = ""
    password: str = ""
    database: str = ""

    @property
    def url(self) -> str:
        return f"{self.dialect}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="DB_",
        env_file=SETTINGS.env_file,
    )

class AWSSettings(BaseSettings):
    access_key_id: str
    secret_access_key: str 
    default_region: str
    s3_bucket: str 
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="AWS_",
        env_file=".env.aws",
    )

class PasswordSettings(BaseSettings):
    secret_for_jwt: str  # JWT 비밀키
    kakao_rest_api_key: str  # 카카오 REST API 키
    gmail_app_password: str

    class Config:
        env_file = ".env.password"
        env_file_encoding = "utf-8"

DB_SETTINGS = DatabaseSettings()
PW_SETTINGS = PasswordSettings()
AWS_SETTINGS = AWSSettings()
