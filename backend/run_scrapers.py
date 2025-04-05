import logging
from typing import List
import time

from scrapers.base_scraper import BaseScraper
from scrapers.mlh_scraper import MlhScraper
from scrapers.mock_scraper import MockScraper
# Import the processing function we will create in Step 4
from inbox_processor import process_scraped_items
from shared_models.models import InboxItem

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_active_scrapers() -> List[BaseScraper]:
    """
    Defines and returns the list of scraper instances to be run.
    This could be configured externally in the future (e.g., via settings or DB).
    """
    scrapers = []
    try:
        # Example: Scrape MLH for the current year + 1 (adjust year as needed)
        from datetime import date
        current_year = date.today().year
        #scrapers.append(MlhScraper(year=current_year)) # Use both current and next year in the future
    except ValueError as e:
        logger.error(f"Failed to initialize MlhScraper: {e}")
    except Exception as e:
        logger.error(f"Unexpected error initializing MlhScraper: {e}")

    # Always include MockScraper for demonstration/testing if needed
    # In production, you might comment this out or control it via settings
    scrapers.append(MockScraper())

    # Add other scrapers here later, e.g.:
    # scrapers.append(DevpostScraper())

    logger.info(f"Initialized {len(scrapers)} active scrapers: {[s.SCRAPER_NAME for s in scrapers]}")
    return scrapers


def run_all_scrapes():
    """
    Runs all active scrapers, collects their results, and passes them to the processor.
    """
    logger.info("Starting scraping cycle...")
    active_scrapers = get_active_scrapers()

    if not active_scrapers:
        logger.warning("No active scrapers configured. Exiting scraping cycle.")
        return

    all_results: List[InboxItem] = []

    for scraper_instance in active_scrapers:
        scraper_name = getattr(scraper_instance, 'SCRAPER_NAME', 'UnknownScraper')
        logger.info(f"--- Running scraper: {scraper_name} ---")
        try:
            # Call the scrape method defined in the BaseScraper interface
            items: List[InboxItem] = scraper_instance.scrape()
            logger.info(f"  -> Scraper {scraper_name} finished. Found {len(items)} potential items.")
            all_results.extend(items)
            time.sleep(1)
        except Exception as e:
            # Catch errors from individual scrapers so one failure doesn't stop all
            logger.error(f"  ERROR running scraper {scraper_name}: {e}", exc_info=True) # Log traceback

    logger.info(f"--- Scraping cycle finished. Collected {len(all_results)} total items. ---")

    # --- Step 4 Placeholder ---
    logger.info("Proceeding to process scraped items...")
    process_scraped_items(all_results)

    logger.info("Scraping and processing initiation complete.")


# Example of how to run this service directly (for testing)
# run this with:
# python -m backend.run_scrapers
# from root in the backend venv
if __name__ == "__main__":
    logger.info("Running scraping service directly...")
    run_all_scrapes()
    logger.info("Direct run finished.")
