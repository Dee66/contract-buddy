from utils.logger_factory import LoggerFactory

def fetch_stackoverflow(api_key, query="python", logger=None):
    """Stub for Stack Overflow API fetch (implement as needed)."""
    logger = logger or LoggerFactory.get_logger("StackOverflowSource")
    logger.debug(f"Fetching Stack Overflow data for query: {query} (API key: {api_key[:4]}...)")
    # Real implementation would use Stack Exchange API
    # https://api.stackexchange.com/docs
    # For now, just log and return empty
    logger.info("Stack Overflow fetch is a stub. No data returned.")
    return []