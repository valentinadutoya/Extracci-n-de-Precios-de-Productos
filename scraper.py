import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_coto(url):
    print(f"Scraping COTO: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    products_data = []
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # COTO's structure can be tricky, this is a common pattern for product cards
        product_cards = soup.find_all('div', class_='product-card') 
        
        if not product_cards:
            print("No product cards found for COTO. Check the HTML structure or URL.")
            
        for card in product_cards:
            name_tag = card.find('div', class_='descrip_full') # Adjust class if needed
            price_tag = card.find('span', class_='atg_store_newPrice') # Adjust class if needed
            url_tag = card.find('a', class_='atg_store_productImage') # Adjust class if needed
            
            name = name_tag.text.strip() if name_tag else 'Nombre no disponible'
            price = price_tag.text.strip() if price_tag else 'Precio no disponible'
            product_url = url_tag['href'] if url_tag and 'href' in url_tag.attrs else 'URL no disponible'
            if product_url != 'URL no disponible' and not product_url.startswith('http'):
                product_url = 'https://www.cotodigital3.com.ar' + product_url
            
            products_data.append(['COTO', name, price, product_url])
            
    except requests.exceptions.RequestException as e:
        print(f"Error accessing COTO: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while scraping COTO: {e}")
        
    return products_data

def scrape_dia(url):
    print(f"Scraping DIA: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    products_data = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # DIA's product structure often involves specific div classes
        product_cards = soup.find_all('div', class_='product-item-info') 
        
        if not product_cards:
            print("No product cards found for DIA. Check the HTML structure or URL.")

        for card in product_cards:
            name_tag = card.find('a', class_='product-item-link') # Adjust class if needed
            price_tag = card.find('span', class_='price') # Adjust class if needed
            
            name = name_tag.text.strip() if name_tag else 'Nombre no disponible'
            price = price_tag.text.strip() if price_tag else 'Precio no disponible'
            product_url = name_tag['href'] if name_tag and 'href' in name_tag.attrs else 'URL no disponible'
            
            products_data.append(['DIA', name, price, product_url])

    except requests.exceptions.RequestException as e:
        print(f"Error accessing DIA: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while scraping DIA: {e}")
        
    return products_data

def scrape_carrefour(url):
    print(f"Scraping Carrefour: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    products_data = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Carrefour's product structure
        product_cards = soup.find_all('article', class_='box-product') 

        if not product_cards:
            print("No product cards found for Carrefour. Check the HTML structure or URL.")
            
        for card in product_cards:
            name_tag = card.find('a', class_='product-card__title') # Adjust class if needed
            price_tag = card.find('p', class_='product-card__price') # Adjust class if needed
            
            name = name_tag.text.strip() if name_tag else 'Nombre no disponible'
            price = price_tag.text.strip() if price_tag else 'Precio no disponible'
            product_url = name_tag['href'] if name_tag and 'href' in name_tag.attrs else 'URL no disponible'
            if product_url != 'URL no disponible' and not product_url.startswith('http'):
                product_url = 'https://www.carrefour.com.ar' + product_url
            
            products_data.append(['Carrefour', name, price, product_url])

    except requests.exceptions.RequestException as e:
        print(f"Error accessing Carrefour: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while scraping Carrefour: {e}")
        
    return products_data

def main():
    print("Iniciando extracción de datos de supermercados...")
    
    supermarket_urls = {
        'DIA': 'https://www.supermercadosdia.com.ar/',
        'COTO': 'https://www.cotodigital3.com.ar/',
        'Carrefour': 'https://www.carrefour.com.ar/'
    }
    
    all_products = []
    
    for supermarket, url in supermarket_urls.items():
        if supermarket == 'COTO':
            products = scrape_coto(url)
        elif supermarket == 'DIA':
            products = scrape_dia(url)
        elif supermarket == 'Carrefour':
            products = scrape_carrefour(url)
        
        all_products.extend(products)
        time.sleep(2) # Be polite, add a delay between requests

    if all_products:
        df = pd.DataFrame(all_products, columns=['Supermercado', 'Producto', 'Precio', 'URL'])
        output_csv = 'productos_supermercados.csv'
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"Extracción completada exitosamente. Datos guardados en {output_csv}")
    else:
        print("No se extrajo ningún producto. Revisa los mensajes de error anteriores.")

if __name__ == "__main__":
    main()