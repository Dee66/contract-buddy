import requests
from utils.logger_factory import LoggerFactory

def fetch_github_repos(repo_list, logger=None):
    """Fetch README files from a list of GitHub repositories."""
    logger = logger or LoggerFactory.get_logger("GitHubSource")
    results = []
    for repo in repo_list:
        url = f"https://api.github.com/repos/{repo}/readme"
        try:
            logger.debug(f"Fetching README from {url}")
            resp = requests.get(url, headers={"Accept": "application/vnd.github.v3.raw"})
            if resp.status_code == 200:
                results.append({"repo": repo, "readme": resp.text})
                logger.info(f"Fetched README for {repo}")
            else:
                logger.warning(f"Failed to fetch {repo}: {resp.status_code}")
        except Exception as e:
            logger.error(f"Exception fetching {repo}: {e}")
    return results