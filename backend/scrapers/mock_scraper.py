from datetime import datetime, timedelta, timezone
from typing import List
from pydantic import HttpUrl

from .base_scraper import BaseScraper
from shared_models.models import InboxItem, DateRange

class MockScraper(BaseScraper):
    """
    A mock scraper that returns a predefined list of InboxItems for testing purposes.
    """
    SCRAPER_NAME = "mock_scraper_v1"

    def __init__(self, scenario: str = "default"):
        """
        Initializes the mock scraper. Can potentially load different scenarios.
        """
        super().__init__()
        self.scenario = scenario
        print(f"Initialized MockScraper (Scenario: {self.scenario})")

    def scrape(self) -> List[InboxItem]:
        """
        Returns a hardcoded list of InboxItem objects based on the scenario.
        """
        print(f"Executing mock scrape logic for {self.SCRAPER_NAME}...")

        # Define some reusable dates and URLs
        now = datetime.now(timezone.utc)
        future_start_1 = now + timedelta(days=30)
        future_end_1 = future_start_1 + timedelta(days=2)
        future_start_2 = now + timedelta(days=60)
        future_end_2 = future_start_2 + timedelta(days=2)
        duplicate_url = HttpUrl("https://example.com/duplicate-hackathon")

        mock_data = [
            # 1. New Item 1 (Looks valid)
            InboxItem(
                name="MockHacks Alpha",
                date=DateRange(start_date=future_start_1, end_date=future_end_1),
                location="Virtual",
                url=HttpUrl("https://example.com/mockhacks-alpha"),
                notes="First test event from mock.",
                source_url=HttpUrl("https://mocksource.com/events"),
                scraper_name=self.SCRAPER_NAME,
            ),
            # 2. New Item 2 (Slightly different)
            InboxItem(
                name="FakeConf Beta",
                date=DateRange(start_date=future_start_2, end_date=future_end_2),
                location="San Francisco, CA",
                url=HttpUrl("https://example.com/fakeconf-beta"),
                source_url=HttpUrl("https://mocksource.com/events"),
                scraper_name=self.SCRAPER_NAME,
                # review_status is defaulted to PENDING in the model
            ),
            # 3. Potential Duplicate Item (Same URL as item 4)
            InboxItem(
                name="Duplicate Event Gamma",
                date=DateRange(start_date=future_start_1, end_date=future_end_1),
                location="Online",
                url=duplicate_url, # Same URL as next item
                notes="This should be caught as a duplicate maybe.",
                source_url=HttpUrl("https://mocksource.com/events"),
                scraper_name=self.SCRAPER_NAME,
            ),
            # 4. Variation Item (Same URL as item 3, different name)
            InboxItem(
                name="Duplicate Event Gamma - Updated Name", # Different name
                date=DateRange(start_date=future_start_1 + timedelta(days=1), end_date=future_end_1 + timedelta(days=1)), # Slightly different date
                location="Online",
                url=duplicate_url, # <<-- SAME URL as previous item
                notes="Variation to test duplicate logic.",
                source_url=HttpUrl("https://mocksource.com/events"),
                scraper_name=self.SCRAPER_NAME,
            ),
            # 5. Item with Missing Optional Data
             InboxItem(
                name="Minimal Event Delta",
                url=HttpUrl("https://example.com/minimal-delta"),
                # Missing date, location, notes
                source_url=HttpUrl("https://mocksource.com/events"),
                scraper_name=self.SCRAPER_NAME,
            ),
             # 6. Item that might fail Pydantic validation (e.g., bad URL string - uncomment to test error handling)
            # InboxItem(
            #    name="Invalid Event Epsilon",
            #    url="not-a-valid-url", # This will likely raise a Pydantic validation error
            #    source_url=HttpUrl("[https://mocksource.com/events"),](https://mocksource.com/events"),)
            #    scraper_name=self.SCRAPER_NAME,
            # ),
        ]

        # You could potentially load different lists based on self.scenario here
        # if self.scenario == "empty":
        #    mock_data = []
        # elif self.scenario == "only_duplicates":
        #    mock_data = [mock_data[2], mock_data[3]]

        print(f"  {self.SCRAPER_NAME} finished. Returning {len(mock_data)} mock items.")
        return mock_data
