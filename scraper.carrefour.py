import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import random

# Configuración
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
DELAY = random.uniform(2, 5)
TIMEOUT = 15
BASE_URL = "https://www.carrefour.com.ar"

def get_page_content(url):
    """Obtiene el contenido HTML con manejo mejorado de errores"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error al acceder a {url}: {str(e)}")
        return None

def extract_carrefour_products():
    """Extrae productos de Carrefour"""
    print("\n🔍 Extrayendo productos de Carrefour...")
    url = f"{BASE_URL}/herramientas-y-ferreteria/pintureria"
    products = []

    soup = get_page_content(url)
    if not soup:
        return []
    
    product_containers = soup.find_all('article', class_='vtex-product-summary-2-x-element')
    
    print(f"Encontrados {len(product_containers)} productos potenciales")
    
    for container in product_containers:
        try:
            # Extraer nombre del producto
            name_element = container.find('span', class_='vtex-product-summary-2-x-productBrand')
            name = name_element.text.strip() if name_element else "Nombre no disponible"
            
            # Extraer precio
            price_element = container.find('span', class_='vtex-product-price-1-x-sellingPrice')
            price = price_element.text.strip() if price_element else "Precio no disponible"
            
            # Extraer URL del producto
            link_element = container.find('a', class_='vtex-product-summary-2-x-clearLink')
            product_url = BASE_URL + link_element['href'] if link_element and 'href' in link_element.attrs else "URL no disponible"
            
            # Extraer precio anterior (tachado)
            old_price_element = container.find('span', class_='vtex-product-price-1-x-listPrice')
            old_price = old_price_element.text.strip() if old_price_element else ""
            
            # Extraer descuento
            discount_element = container.find('span', class_='vtex-product-price-1-x-savings')
            discount = discount_element.text.strip() if discount_element else ""
            
            products.append({
                'Supermercado': 'Carrefour',
                'Producto': name,
                'Precio Actual': price,
                'Precio Anterior': old_price,
                'Descuento': discount,
                'URL': product_url
            })
            
            print(f"✅ Añadido: {name[:30]}... - {price} (Descuento: {discount})")
            
        except Exception as e:
            print(f"⚠️ Error procesando producto: {str(e)}")
            continue
    
    return products

def save_to_csv(products, filename="productos_carrefour.csv"):
    """Guarda los productos en un archivo CSV"""
    if not products:
        print("No se encontraron productos para guardar.")
        return
    
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n💾 Datos guardados en '{filename}'")
    print(f"📊 Total de productos: {len(df)}")

if __name__ == "__main__":
    products = extract_carrefour_products()
    save_to_csv(products)
