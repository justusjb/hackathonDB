from .base_scraper import BaseScraper
from shared_models.models import InboxItem, DateRange
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_daterange(start_str: str | None, end_str: str | None) -> DateRange | None:
    """Parses YYYY-MM-DD date strings into a DateRange object."""
    if not start_str or not end_str:
        logger.warning("Warning: Missing start or end date string.")
        return None
    try:
        # Parse date strings, assume UTC timezone for consistency
        start_dt = datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_dt = datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return DateRange(start_date=start_dt, end_date=end_dt)
    except ValueError as e:
        logger.error(f"Error parsing dates '{start_str}', '{end_str}': {e}")
        return None


class MlhScraper(BaseScraper):
    BASE_URL_TEMPLATE = "https://mlh.io/seasons/{year}/events"
    HEADERS = {
         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }
    def __init__(self, year: int):
        """
        Initializes the scraper for a specific MLH season year.

        Args:
            year: The season year (e.g. 2025, 2026).
        """
        super().__init__() # Call parent __init__ if BaseScraper has one (currently doesn't, but good practice)
        if not isinstance(year, int) or year < 2000: # Basic validation
            raise ValueError("Invalid year provided for MLH Scraper")

        self.year = year
        self.target_url = self.BASE_URL_TEMPLATE.format(year=self.year)
        self.SCRAPER_NAME = f"mlh_events_{self.year}_inperson"
        logger.info(f"Initialized MlhScraper for year {self.year} ({self.target_url})")


    def scrape(self) -> List[InboxItem]:
        logger.info(f"Executing specific scrape logic for {self.SCRAPER_NAME}...")
        scraped_items: List[InboxItem] = []

        try:
            response = requests.get(self.target_url, headers=self.HEADERS, timeout=15)
            logger.info("Status:", response.status_code)
            logger.info("First 1000 chars of response:", response.text[:1000])
            response.raise_for_status() # Raise error if there is an HTTP error
            soup = BeautifulSoup(response.content, 'lxml')
            logger.info("  Successfully fetched and parsed MLH page.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {self.target_url}: {e}")
            return []

        # --- Find upcoming events container ---
        upcoming_events_container = None
        section_containers = soup.find_all('div', class_='row')
        for container in section_containers:
             heading = container.find('h3', recursive=False)
             if heading and 'Upcoming Events' in heading.get_text():
                  upcoming_events_container = container
                  break

        if not upcoming_events_container:
            logger.warning("  Could not find MLH upcoming events container.")
            return []

        # --- Select and filter cards ---
        event_card_selector = 'div.col-lg-3.col-md-4.col-sm-6'
        all_upcoming_cards = upcoming_events_container.select(event_card_selector)
        logger.info(f"  Found {len(all_upcoming_cards)} total upcoming cards. Filtering for in-person...")

        in_person_cards = []
        for card in all_upcoming_cards:
             in_person_tag = card.select_one("div.event-hybrid-notes span")
             if in_person_tag and "In-Person Only" in in_person_tag.get_text(strip=True):
                  in_person_cards.append(card)

        logger.info(f"  Found {len(in_person_cards)} in-person cards. Parsing...")

        # --- Extract data using selectors based on the provided HTML ---
        for card in in_person_cards:
            name_tag = card.select_one('h3.event-name')
            name = name_tag.get_text(strip=True) if name_tag else None

            link_tag = card.select_one('a.event-link')
            hackathon_url = link_tag['href'] if link_tag and link_tag.has_attr('href') else None

            start_date_tag = card.select_one('meta[itemprop="startDate"]')
            start_date_str = start_date_tag['content'] if start_date_tag and start_date_tag.has_attr('content') else None

            end_date_tag = card.select_one('meta[itemprop="endDate"]')
            end_date_str = end_date_tag['content'] if end_date_tag and end_date_tag.has_attr('content') else None

            city_tag = card.select_one('span[itemprop="city"]')
            city = city_tag.get_text(strip=True) if city_tag else None

            state_tag = card.select_one('span[itemprop="state"]')
            state = state_tag.get_text(strip=True) if state_tag else None

            # Combine City and State for location string
            location_parts = [part for part in [city, state] if part]
            location = ", ".join(location_parts) if location_parts else None

            # --- Create DateRange object ---
            date_range = create_daterange(start_date_str, end_date_str)

            # --- Assemble data for InboxItem ---
            item_data = {
                "name": name,
                "date": date_range, # Use the Pydantic DateRange object
                "location": location,
                "url": hackathon_url, # This is the direct hackathon link
                "notes": None,
                # Status isn't usually available on the list page
                "source_url": self.target_url, # The page where we found this item
                "scraper_name": self.SCRAPER_NAME, # Identify the scraper
            }

            try:
                # Filter out None values *before* passing to Pydantic
                valid_item_data = {k: v for k, v in item_data.items() if v is not None}
                inbox_item = InboxItem(**valid_item_data)
                scraped_items.append(inbox_item)
            except Exception as e:
                logger.error(f"  Error creating InboxItem for {name}: {e}")
                logger.error(f"  Data: {valid_item_data}")
                
        logger.info(f"  {self.SCRAPER_NAME} finished. Found {len(scraped_items)} items.")
        return scraped_items
