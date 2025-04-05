import logging
from typing import List

from pymongo.database import Database
from pymongo.errors import DuplicateKeyError # Good to handle just in case

# Adjust import paths as needed
from database import get_db
from shared_models.models import InboxItem, InboxStatus

# Get logger instance (child logger of the one in run_scrapers if run via that)
logger = logging.getLogger(__name__)

def is_duplicate(item: InboxItem, db: Database) -> bool:
    """
    Checks if an item with the same URL already exists in the inbox or main hackathon collection.

    Args:
        item: The InboxItem to check.
        db: The database instance.

    Returns:
        True if a duplicate is found, False otherwise.
    """
    if not item.url:
        logger.warning(f"InboxItem '{item.name}' has no URL, cannot check for duplicates based on URL.")
        return False

    query_url = str(item.url)

    # Check 1: Exists in inbox collection (regardless of status)
    inbox_collection = db['inbox']
    existing_inbox = inbox_collection.find_one({"url": query_url})
    if existing_inbox:
        logger.debug(f"Duplicate found in inbox: URL='{query_url}', Name='{item.name}', Existing ID='{existing_inbox.get('_id')}'")
        return True

    # Check 2: Exists in the main hackathons collection
    hackathons_collection = db['hackathons']
    existing_hackathon = hackathons_collection.find_one({"url": query_url})
    if existing_hackathon:
        logger.debug(f"Duplicate found in main collection: URL='{query_url}', Name='{item.name}', Existing ID='{existing_hackathon.get('_id')}'")
        return True

    # If not found in either collection
    return False


def process_scraped_items(items: List[InboxItem]):
    """
    Processes a list of scraped InboxItems, checks for duplicates,
    and inserts new items into the 'inbox' database collection.
    """
    if not items:
        logger.info("No items to process.")
        return

    logger.info(f"Starting processing of {len(items)} scraped items...")
    db = get_db()
    inbox_collection = db['inbox']

    inserted_count = 0
    skipped_count = 0

    for item in items:
        try:
            # Ensure status is PENDING before check/insert
            item.review_status = InboxStatus.PENDING

            if is_duplicate(item, db):
                logger.info(f"Skipping duplicate item: URL='{item.url}', Name='{item.name}'")
                skipped_count += 1
                continue

            # Item is new, prepare for insertion
            # Convert Pydantic model to dict for MongoDB insertion
            # Use exclude_unset=True? Or default values are fine? Let's keep defaults for now.
            # Use by_alias=True if your model uses aliases like '_id'
            item_dict = item.model_dump(mode='python', by_alias=True)

            # Remove '_id' if it's None, MongoDB will generate one
            if '_id' in item_dict and item_dict['_id'] is None:
                del item_dict['_id']

            logger.debug(f"Attempting to insert new item: {item_dict.get('name')}")
            insert_result = inbox_collection.insert_one(item_dict)
            logger.info(f"Successfully inserted new item: Name='{item.name}', DB_ID='{insert_result.inserted_id}'")
            inserted_count += 1

        except DuplicateKeyError:
             # This might happen in rare race conditions or if duplicate check logic is imperfect
             logger.warning(f"DuplicateKeyError on inserting item (likely race condition or check mismatch): URL='{item.url}', Name='{item.name}'")
             skipped_count += 1
        except Exception as e:
            item_name = getattr(item, 'name', 'UNKNOWN')
            logger.error(f"Failed to process item: Name='{item_name}', URL='{getattr(item, 'url', 'N/A')}' - Error: {e}", exc_info=True)
            # Decide if you want to count this as skipped or handle differently
            skipped_count += 1


    logger.info(f"Finished processing items. Inserted: {inserted_count}, Skipped (Duplicates/Errors): {skipped_count}")
