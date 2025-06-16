"""
Data Versioning Script for Contract Buddy
-----------------------------------------
Handles dataset versioning for reproducibility and auditability.
"""

from pathlib import Path
from typing import Dict
from utils.logger_factory import LoggerFactory
import subprocess
import datetime

class DataVersioning:
    """
    Handles dataset versioning for reproducibility and auditability.
    """
    def __init__(self, config: Dict):
        self.config = config
        self.logger = LoggerFactory.get_logger(self.__class__.__name__, config)
        self.clean_data_dir = Path(self.config["paths"]["clean_data"])

    def version_data(self) -> None:
        """
        Version the cleaned data directory using Git or DVC.
        """
        self.logger.info("Starting data versioning...")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            # Example: Using Git for versioning
            subprocess.run(["git", "add", str(self.clean_data_dir)], check=True)
            commit_msg = f"Update cleaned data version ({self.clean_data_dir}) at {timestamp}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            self.logger.info(f"Data versioned and committed: {self.clean_data_dir} at {timestamp}")
            # For DVC, you could add: subprocess.run(["dvc", "add", str(self.clean_data_dir)], check=True)
        except subprocess.CalledProcessError as e:
            self.logger.exception(f"Versioning failed: {e}")
        except Exception as e:
            self.logger.exception(f"Unexpected error during versioning: {e}")

        self.logger.info("Data versioning completed.")

if __name__ == "__main__":
    import sys
    from utils.utils import read_yaml
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    config = read_yaml(config_path)
    versioner = DataVersioning(config)
    versioner.version_data()