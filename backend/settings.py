from pydantic_settings import BaseSettings
from typing import Literal
from pathlib import Path


DOTENV_PATH = Path(__file__).parent / '.env'


class Settings(BaseSettings):
    # Environment configuration
    ENVIRONMENT: Literal["production", "staging"] 
    MONGODB_URI: str
    ADMIN_API_KEY: str
    
    # Computed properties
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def mongodb_database(self) -> str:
        return "hackathons_prod" if self.is_production else "hackathons_test_1"
    
    class Config:
        env_file = DOTENV_PATH
        case_sensitive = False

# Create a global settings instance
settings = Settings()
