from pydantic_settings import BaseSettings
from typing import Literal
from pathlib import Path
import os

DOTENV_PATH = Path(__file__).parent / '.env'


class Settings(BaseSettings):
    # Environment configuration
    ENVIRONMENT: Literal["production", "staging", "test"] 
    MONGODB_URI: str
    ADMIN_API_KEY: str
    
    # Computed properties
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_testing(self) -> bool:
        # Check if pytest is running via standard env var it can set
        return os.getenv("PYTEST_RUNNING") == "1" or self.ENVIRONMENT == "test"
    
    @property
    def mongodb_database(self) -> str:
        if self.is_testing:
            return "hackathons_pytest"
        elif self.is_production:
            return "hackathons_prod"
        else:
            return "hackathons_test_1"
    
    class Config:
        env_file = DOTENV_PATH
        case_sensitive = False

# Create a global settings instance
settings = Settings()
