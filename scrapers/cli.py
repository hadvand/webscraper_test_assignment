import argparse
from notino.scraper import NotinoScraper
from notino.transformation import transform_data


def main():
    """
    Entry point for the Notino Scraper and Transformer CLI.
    """
    parser = argparse.ArgumentParser(description="Notino Scraper and Transformer CLI")
    parser.add_argument('action', choices=['scrape', 'transform'], help="Action to perform: scrape or transform")

    args = parser.parse_args()

    if args.action == 'scrape':
        scraper = NotinoScraper('https://www.notino.cz/zubni-pasty/')
        scraper.get_info()
    elif args.action == 'transform':
        transform_data()


if __name__ == "__main__":
    main()
