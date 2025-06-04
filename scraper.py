from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

# Configuración de Selenium
options = Options()
options.add_argument('--headless')  # Ejecuta Chrome en modo headless (sin interfaz gráfica)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Reemplaza 'path_to_chromedriver' con la ruta a tu ChromeDriver
service = Service(executable_path='path_to_chromedriver')
driver = webdriver.Chrome(service=service, options=options)

# Lista de URLs de productos
urls = [
    "https://www.cotodigital3.com.ar/sitios/cdigi/producto/_/A-00490026-00490026-200/",
    "https://www.cotodigital3.com.ar/sitios/cdigi/producto/_/A-00490025-00490025-200/",
    "https://www.cotodigital3.com.ar/sitios/cdigi/producto/_/A-00501938-00501938-200/",
    "https://www.cotodigital3.com.ar/sitios/cdigi/producto/_/A-00512265-00512265-200/"
]

# Crear y escribir en el archivo CSV
with open('productos_scrapeados.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Supermercado', 'Producto', 'Precio', 'URL'])

    for url in urls:
        driver.get(url)
        time.sleep(5)  # Espera a que la página cargue completamente

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extraer el nombre del producto
        nombre_tag = soup.find('h1')
        nombre = nombre_tag.get_text(strip=True) if nombre_tag else 'No encontrado'

        # Extraer el precio del producto
        precio_tag = soup.find('span', class_='product-price')
        if not precio_tag:
            # Buscar un span que contenga el símbolo '$'
            precio_tag = soup.find('span', string=lambda text: '$' in text if text else False)
        precio = precio_tag.get_text(strip=True) if precio_tag else 'No encontrado'

        writer.writerow(['Coto', nombre, precio, url])

driver.quit()
