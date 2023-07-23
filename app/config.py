from pydantic import BaseSettings

# schema for all environment variables  
class Settings(BaseSettings):
    database_hostname: str 
    database_port: str
    database_password: str 
    database_name: str 
    database_username: str
    secret_key: str # for json web token 
    algorithm: str  # for signing token 
    access_token_expire_minutes: int 

    class Config: 
        env_file = '.env'
        case_sensitive = False

settings = Settings() # instance of Setting class
# print(settings.database_password) 