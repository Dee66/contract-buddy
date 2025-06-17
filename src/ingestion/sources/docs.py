import requests
from src.utils.logger_factory import LoggerFactory

def fetch_docs(doc_urls, logger=None):
    """Fetch documentation pages (simplified example)."""
    logger = logger or LoggerFactory.get_logger("DocsSource")
    docs = []
    for url in doc_urls:
        try:
            logger.debug(f"Fetching documentation from {url}")
            resp = requests.get(url)
            if resp.status_code == 200:
                docs.append({"url": url, "content": resp.text})
                logger.info(f"Fetched documentation from {url}")
            else:
                logger.warning(f"Failed to fetch {url}: {resp.status_code}")
        except Exception as e:
            logger.error(f"Exception fetching {url}: {e}")
    return docs