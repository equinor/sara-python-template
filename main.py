"""Entry point for the sara-service.

Replace this stub with the CLI/HTTP entry point for your service.
"""

import logging

from sara_service import __version__


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    logging.info("sara-service version=%s started", __version__)


if __name__ == "__main__":
    main()
