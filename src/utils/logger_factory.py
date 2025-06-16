import logging
from pathlib import Path

class LoggerFactory:
    @staticmethod
    def get_logger(name: str, config: dict = None):
        logger = logging.getLogger(name)
        if not logger.handlers:
            log_level = logging.INFO
            log_file = "pipeline.log"
            if config and "logging" in config:
                level_str = config["logging"].get("level", "INFO").upper()
                log_level = getattr(logging, level_str, logging.INFO)
                log_file = config["logging"].get("log_file", "pipeline.log")
            log_dir = config["paths"]["logs"] if config and "paths" in config else "logs"
            Path(log_dir).mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(Path(log_dir) / log_file)
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(log_level)
        return logger