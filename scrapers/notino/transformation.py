import pandas as pd
import os


def transform_data(country: str = 'Czech Republic', currency: str = 'CZK') -> None:
    """
    Transforms the raw scraped data to the final format with additional fields

    :param country: Country for the transformation
    :param currency: Currency for the transformation
    """
    input_file = 'data/notino_raw.csv'
    output_file = 'data/notino_transformed.csv'

    df = pd.read_csv(input_file)
    df['Country'] = country
    df['Currency'] = currency
    df['Discount_Amount'] = df['Discount']

    os.makedirs('data', exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')


if __name__ == "__main__":
    transform_data()
