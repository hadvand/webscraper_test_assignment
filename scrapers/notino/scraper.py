import os
from typing import List, Optional
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from abstract.abstract_scraper import AbstractScraper


class Product:
    """
    Class representing a product scraped from Notino.
    """

    def __init__(self, name: str, brand: str, original_price: str, url: str, image: str, discount: str,
                 discounted_price: str, scraped_at: str):
        self.name = name
        self.brand = brand
        self.original_price = original_price
        self.url = url
        self.image = image
        self.discount = discount
        self.discounted_price = discounted_price
        self.scraped_at = scraped_at


class NotinoScraper(AbstractScraper):
    """
    Scraper for extracting product information from Notino.
    """

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def get_info(self) -> None:
        """
        Main method to scrape the products and save them to a CSV file.
        """
        page_number = 1
        products = []
        scraped_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            url = self.base_url if page_number == 1 else f"{self.base_url}?f={page_number}-1-2-4891-7183"
            self.logger.info(f"Scraping {url}")
            html = self.send_get_request(url)
            if not html:
                break

            soup = BeautifulSoup(html, 'html.parser')
            new_products = self.parse_products(soup, scraped_at)
            if not new_products:
                break

            products.extend(new_products)
            page_number += 1

        self.save_result(products)

    @staticmethod
    def parse_products(soup: BeautifulSoup, scraped_at: str) -> List[Product]:
        """
        Parses the HTML to extract product information.

        :param soup: BeautifulSoup object containing the HTML
        :param scraped_at: The timestamp when the information was scraped
        :return: List of Product objects
        """
        products = []
        product_elements = soup.select(
            'div.sc-bSstmL.sc-bYpRZF.iJzxKb.llgfxg.styled__StyledProductTile-sc-1i2ozu3-0.dhBqlM')

        for product in product_elements:
            url_tag = product.select_one('a.sc-jdHILj.OFtqG')
            url = f"https://www.notino.cz{url_tag['href']}" if url_tag else None

            image_tag = product.select_one('img')
            image_url = image_tag['src'] if image_tag else None

            brand_tag = product.select_one('h2.sc-guDLey')
            brand = brand_tag.text if brand_tag else None

            product_name_tag = product.select_one('h3.sc-dmyCSP')
            product_name = product_name_tag.text if product_name_tag else None

            original_price_tag = product.select_one('span[data-testid="price-component"]')
            original_price = original_price_tag.text.replace(' ', '').replace('Kč', '') if original_price_tag else None

            discount_percent_tag = product.select_one('span.styled__DiscountValue-sc-1b3ggfp-1')
            discount_percent = discount_percent_tag.text.replace('%', '').strip() if discount_percent_tag else '0'

            # Calculate discounted price using discount percent
            discounted_price_value = '0'
            discount_value = '0 Kč'
            if original_price and discount_percent:
                try:
                    original_price_value = float(original_price)
                    discount_percent_value = float(discount_percent) / 100
                    discounted_price_value = original_price_value * (1 - discount_percent_value)
                    discount_value = f"{original_price_value - discounted_price_value:.2f} Kč"
                    discounted_price_value = f"{discounted_price_value:.2f} Kč"
                except ValueError:
                    discount_value = '0 Kč'
                    discounted_price_value = '0 Kč'

            original_price_with_currency = f"{original_price} Kč" if original_price else 'Nedostupne'

            products.append(Product(product_name, brand, original_price_with_currency, url, image_url, discount_value,
                                    discounted_price_value, scraped_at))

        return products

    def save_result(self, products: List[Product]) -> None:
        """
        Saves the product information to a CSV file.

        :param products: List of Product objects to save
        """
        self.logger.info("Saving results to CSV...")
        os.makedirs('data', exist_ok=True)

        data = [
            {
                'Name': product.name,
                'Brand': product.brand,
                'Original Price': product.original_price,
                'URL': product.url,
                'Image': product.image,
                'Discount': product.discount,
                'Discounted Price': product.discounted_price,
                'Scraped At': product.scraped_at
            }
            for product in products
        ]

        df = pd.DataFrame(data)
        df.to_csv('data/notino_raw.csv', index=False, encoding='utf-8')

        self.logger.info("Results saved successfully.")


if __name__ == "__main__":
    scraper = NotinoScraper('https://www.notino.cz/zubni-pasty/')
    scraper.get_info()
