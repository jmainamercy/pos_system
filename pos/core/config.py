import os

class SecuritySettings:
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super_secret_pos_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480 

security_settings = SecuritySettings()
