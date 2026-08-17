import logging
import time
import sys

from config.settings import LOGS_PATH
from src.extract import fetch_all_weather
from src.transform import flatten
from src.load import load_all

def setup_logging() -> None:
    LOGS_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler(LOGS_PATH),
            logging.StreamHandler(sys.stdout),
        ]
    )

def run() -> None:

    start_time = time.time()
    logging.info("===Starting Weather Pipeline===")

    try:
        logging.info("Step 1/3: Extracting raw data...")
        raw = fetch_all_weather()
        
        if not raw:
            logging.error(
                "Extraction failed: No data retrieved from API."
            )
            sys.exit(1)
        
        logging.info("Step 2/3: Transforming raw JSON payloads...")
        clean = flatten(raw)

        if clean.empty:
            logging.error(
                "Transformation failed: Data Frame is empty"
            )
            sys.exit(1)
        
        logging.info("Step 3/3: Loading clean data to database and excel...")
        load_all(clean)

        elapsed_time = round(time.time() - start_time, 2)
        logging.info(f"=== Pipeline executed succesfully in {elapsed_time}s ===")

    except Exception as err:
        logging.critical(
            f"Pipeline failed due to unhandled error: {err}", exc_info=True
        )
        sys.exit(1)

if __name__ == "__main__":
    setup_logging()
    run()
