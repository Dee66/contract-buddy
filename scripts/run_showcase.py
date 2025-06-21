import os
import sys
import yaml
from utils.environment import setup_logging

setup_logging()
logging = __import__("logging")
sys.path.insert(0, os.path.abspath("."))


def load_and_set_env(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    env = config.get("environment", "dev")
    os.environ["MODE"] = env  # For legacy code
    os.environ["CB_ENV"] = env  # For new code
    logging.info(f"Loaded config and set environment: {env}")


if __name__ == "__main__":
    load_and_set_env()
    logging.info("Starting CodeCraft AI Showcase pipeline from run_showcase.py")
    try:
        from scripts.run_showcase_pipeline import main

        main()
        logging.info("CodeCraft AI Showcase pipeline finished")
    except Exception as e:
        logging.exception(f"Pipeline failed with an unexpected error: {e}")
        sys.exit(1)
