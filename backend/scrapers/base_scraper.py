from abc import ABC, abstractmethod
from typing import List
# Adjust import path based on your project structure and how you installed shared_models
from shared_models.models import InboxItem

class BaseScraper(ABC):
    """Abstract base class for all website scrapers."""

    # Class attribute to identify the scraper (optional but useful)
    SCRAPER_NAME = "base"

    @abstractmethod
    def scrape(self) -> List[InboxItem]:
        """
        Scrapes the target website and returns a list of potential InboxItem objects.
        Implementations should handle fetching, parsing, and basic data structuring.
        Duplicate checking and database interaction should ideally happen outside this method.
        """
        pass

    # You could add common helper methods here if needed later