import pandas as pd
import re

EXCHANGE_RATE = 16000

dirty_patterns = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5", "Not Rated"],
    "Price": ["Price Unavailable", None]
}

def transform_data(file_path='products.csv'):

    df = pd.read_csv(file_path)

    for column, patterns in dirty_patterns.items():
        df = df[~df[column].isin(patterns)]

    df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float) * EXCHANGE_RATE

    def clean_rating(value):
        if isinstance(value, str):
            match = re.search(r'(\d+(\.\d+)?)', value)
            return float(match.group(1)) if match else None
        else:
            return None

    df['Rating'] = df['Rating'].apply(clean_rating)
    df = df.dropna(subset=['Rating']) 

    def clean_colors(value):
        if isinstance(value, str):
            match = re.search(r'(\d+)', value)
            return int(match.group(1)) if match else None
        else:
            return None


    df['Colors'] = df['Colors'].apply(clean_colors)
    df = df.dropna(subset=['Colors'])  

    df['Size'] = df['Size'].str.replace('Size: ', '')
    df['Gender'] = df['Gender'].str.replace('Gender: ', '')

    df.drop_duplicates(inplace=True)

    df = df.astype({
        'Title': 'object',
        'Price': 'float64',
        'Rating': 'float64',
        'Colors': 'int64',
        'Size': 'object',
        'Gender': 'object'
    })

    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'

    return df
