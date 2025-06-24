import os
import sys
from src.adapters.environment import get_config  # type: ignore

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def main():
    """
    Performs a health check on the application.
    Exits with status 0 if healthy, 1 otherwise.
    """
    try:
        config = get_config()
        if config and config.get("vector_repository"):
            print("Health check passed: Configuration loaded successfully.")
            sys.exit(0)
        else:
            print("Health check failed: Configuration is empty or invalid.")
            sys.exit(1)
    except Exception as e:
        print(f"Health check failed with exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
