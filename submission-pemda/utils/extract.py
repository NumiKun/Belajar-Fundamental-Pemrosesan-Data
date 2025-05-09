import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def extract_data():
    all_data = []
    
    extraction_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    url_first_page = 'https://fashion-studio.dicoding.dev/'
    try:
        response = requests.get(url_first_page, timeout=10)  
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        process_page(soup, all_data, extraction_timestamp)
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving the first page: {e}")
    
    # Halaman 2 hingga 50
    for page_num in range(2, 51):
        url = f'https://fashion-studio.dicoding.dev/page{page_num}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            process_page(soup, all_data, extraction_timestamp)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from page {page_num}: {e}")
    
    save_to_csv(all_data)

def process_page(soup, all_data, timestamp):
    products = soup.find_all('div', class_='collection-card')
    
    for product in products:
        try:
            title = product.find('h3', class_='product-title').get_text() if product.find('h3', class_='product-title') else 'N/A'
            
            price = 'N/A'
            price_container = product.find('div', class_='price-container')
            if price_container:
                price = price_container.find('span', class_='price').get_text() if price_container.find('span', class_='price') else 'Price Unavailable'
            else:
                price_tag = product.find('p', class_='price')
                price = price_tag.get_text() if price_tag else 'Price Unavailable'
            
            details = product.find('div', class_='product-details')
            rating = details.find('p', string=lambda text: text and 'Rating' in text).get_text() if details and details.find('p', string=lambda text: text and 'Rating' in text) else 'N/A'
            colors = details.find('p', string=lambda text: text and 'Colors' in text).get_text() if details and details.find('p', string=lambda text: text and 'Colors' in text) else 'N/A'
            size = details.find('p', string=lambda text: text and 'Size' in text).get_text() if details and details.find('p', string=lambda text: text and 'Size' in text) else 'N/A'
            gender = details.find('p', string=lambda text: text and 'Gender' in text).get_text() if details and details.find('p', string=lambda text: text and 'Gender' in text) else 'N/A'
            
            all_data.append([title, price, rating, colors, size, gender, timestamp])
        except Exception as e:
            print(f"Error processing product: {e}")

def save_to_csv(data):
    try:
        header = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
        with open('submission-pemda/products.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)
        print("Data successfully saved to 'products.csv'.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

extract_data()
