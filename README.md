# Notino Scraper and Transformer

## General Info

This project provides a command-line interface (CLI) for scraping toothpaste product data from the Notino website and transforming the data into a specified format.

## Project Structure
```
scrapers/
│
├── abstract/
│ └── abstract_scraper.py # Base class for scrapers.
│
├── notino/
│ ├── scraper.py # Scraper for Notino - raw data.
│ └── transformation.py # Transformation of raw data to final format.
│
├── data/
│ ├── notino_raw.csv # Raw scraped data.
│ └── notino_transformed.csv # Transformed data.
│
├── cli.py # Entry point for the CLI.
└── README.md # Documentation of the project.
```

## Installation

1. **Enter the directory:**

    ```sh
    cd scrapers
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate # works on linux
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Scraping Data

To scrape data from Notino, use the `scrape` action with the `cli.py` script. scrape.

```sh
python cli.py scrape
```

This will save the raw scraped data to `data/notino_raw.csv`.

### Transforming Data

To transform the raw scraped data into the final format, use the transform action with the cli.py script. You can specify the country and currency for the transformation.

```sh
python cli.py transform
```

This will save the transformed data to `data/notino_transformed.csv`.

### Code Overview

#### abstract/abstract_scraper.py

This file contains the AbstractScraper class, which provides logging and methods for sending GET and POST requests.

#### notino/scraper.py
    
This file contains the NotinoScraper class, which inherits from AbstractScraper and implements the `get_info`, `parse_products`, and `save_result` methods for scraping toothpaste product data from Notino.

#### notino/transformation.py

This file contains the transform_data function, which reads the raw data from `notino_raw.csv`, adds additional fields, and saves the transformed data to `notino_transformed.csv`.

#### cli.py

This file contains the CLI implementation using argparse. It supports two actions: scrape and transform.
