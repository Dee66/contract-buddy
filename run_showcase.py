import os
import sys
from src.utils.environment import setup_logging

setup_logging()
logging = __import__("logging")
sys.path.insert(0, os.path.abspath("."))

if __name__ == "__main__":
    logging.info("Starting Contract Buddy Showcase pipeline from run_showcase.py")
    try:
        from src.scripts.run_showcase_pipeline import main
        main()
        logging.info("Contract Buddy Showcase pipeline finished")
    except Exception as e:
        logging.exception(f"Pipeline failed with an unexpected error: {e}")
        sys.exit(1)