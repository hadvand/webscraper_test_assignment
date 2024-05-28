import logging
import time
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class AbstractScraper:
    """
    Abstract base class for scrapers, providing logging and HTTP request methods.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def send_get_request(self, url: str, retries: int = 10) -> Optional[str]:
        """
        Sends a GET request to the specified URL with retry logic for errors.

        :param url: URL to send the request to
        :param retries: Number of times to retry the request
        :return: Response text if the request is successful, otherwise None
        """

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        for attempt in range(retries):
            try:
                req = Request(url, headers=headers)
                with urlopen(req) as response:
                    return response.read().decode('utf-8')
            except HTTPError as e:
                self.logger.error(f"HTTP error fetching {url}: {e}")
            except URLError as e:
                self.logger.error(f"URL error fetching {url}: {e}")
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {e}")

            if attempt < retries - 1:
                self.logger.info(f"Retrying in a moment... (Attempt {attempt + 1} of {retries})")
                time.sleep(0.5)
            else:
                self.logger.error(f"All {retries} attempts failed for {url}.")
        return None

    def send_post_request(self, url: str, data: Optional[dict] = None) -> Optional[str]:
        """
        Sends a POST request to the specified URL.

        :param url: URL to send the request to
        :param data: Optional data for the request
        :return: Response text if the request is successful, otherwise None
        """

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        try:
            req = Request(url, data=data, headers=headers, method='POST')
            with urlopen(req) as response:
                return response.read().decode('utf-8')
        except HTTPError as e:
            self.logger.error(f"HTTP error posting to {url}: {e}")
        except URLError as e:
            self.logger.error(f"URL error posting to {url}: {e}")
        except Exception as e:
            self.logger.error(f"Error posting to {url}: {e}")
        return None
