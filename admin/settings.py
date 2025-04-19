from pydantic_settings import BaseSettings
from typing import Literal
from pathlib import Path
import os

DOTENV_PATH = Path(__file__).parent / '.env'


class Settings(BaseSettings):
    ENVIRONMENT: Literal["production", "staging", "test"] 
    MONGODB_URI: str
    OPENCAGE_API_KEY: str
    ADMIN_API_KEY: str
    BACKEND_URL_PROD: str
    BACKEND_URL_STAGING: str
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_testing(self) -> bool:
        return os.getenv("PYTEST_RUNNING") == "1" or self.ENVIRONMENT == "test"
    
    @property
    def mongodb_database(self) -> str:
        if self.is_testing:
            return "hackathons_pytest"
        elif self.is_production:
            return "hackathons_prod"
        else:
            return "hackathons_test_1"

    @property
    def BACKEND_URL(self):
        if self.ENVIRONMENT == "production":
            return self.BACKEND_URL_PROD
        return self.BACKEND_URL_STAGING

    def update_environment(self, new_environment: Literal["production", "staging"]) -> None:
        """
        Update the environment setting.
        This method ensures the change survives application restarts.
        
        Args:
            new_environment: The new environment to set (either "production" or "staging")
        """
        # Don't allow changing to test environment through this method
        if new_environment not in ["production", "staging"]:
            raise ValueError("Environment must be either 'production' or 'staging'")
        
        # Update the current instance
        self.ENVIRONMENT = new_environment
    
    model_config = {
        "env_file": DOTENV_PATH,
        "case_sensitive": False,
    }

# Create a global settings instance
settings = Settings()
