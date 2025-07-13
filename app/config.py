from pydantic_settings import BaseSettings, SettingsConfigDict




class DatabaseSettings(BaseSettings):

    POSTGRES_SERVER:str
    POSTGRES_PORT:int
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str


    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        #ve dire prend seulement les variable dans les annoations en haut depuis .env et ingore les autre variabels
        extra="ignore",
        )
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )



settings = DatabaseSettings()

print(settings.POSTGRES_URL)