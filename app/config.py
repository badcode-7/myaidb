from pydantic import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "auth_user"
    db_password: str = "auth_password"
    db_name: str = "auth_db"
    
    # JWT配置
    secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()