import re
from typing import List, Any
from src.utils.logger_factory import LoggerFactory

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",  # AWS Access Key ID
    r"(?i)api[_-]?key\s*[:=]\s*[A-Za-z0-9\-]{16,}",  # API keys
    r"(?i)password\s*[:=]\s*.+",  # Passwords
    r"(?i)secret\s*[:=]\s*.+",  # Secrets
    r"(?i)token\s*[:=]\s*.+",  # Tokens
]

class SensitiveDataFilter:
    def __init__(self, logger=None):
        self.logger = logger or LoggerFactory.get_logger(self.__class__.__name__)

    def contains_sensitive_data(self, text: str) -> bool:
        for pattern in SECRET_PATTERNS:
            if re.search(pattern, text):
                self.logger.debug(f"Sensitive pattern matched: {pattern} in text: {text[:50]}")
                return True
        return False

    def filter_sensitive_entries(self, entries: List[Any]) -> List[Any]:
        filtered = []
        for e in entries:
            if not self.contains_sensitive_data(str(e)):
                filtered.append(e)
            else:
                self.logger.info(f"Filtered sensitive entry: {str(e)[:50]}")
        return filtered

# For backward compatibility with procedural usage:
_filter = SensitiveDataFilter()
contains_sensitive_data = _filter.contains_sensitive_data
filter_sensitive_entries = _filter.filter_sensitive_entries