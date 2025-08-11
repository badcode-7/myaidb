# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # 读取 .env；忽略额外变量，避免报错
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # 数据库配置（使用 env 名作为校验别名，兼容你 .env/compose）
    db_host: str = Field("localhost", validation_alias="DB_HOST")
    db_port: int = Field(3306, validation_alias="DB_PORT")
    db_user: str = Field("auth_user", validation_alias="DB_USER")
    db_password: str = Field("auth_password", validation_alias="DB_PASSWORD")
    db_name: str = Field("auth_db", validation_alias="DB_NAME")

    # JWT配置
    secret_key: str = Field("change-me", validation_alias="SECRET_KEY")
    algorithm: str = Field("HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    @property
    def sqlalchemy_database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()
