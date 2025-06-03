import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Definimos los sitios a scrapear
supermercados = {
    "COTO": "https://www.cotodigital3.com.ar/sitios/cdigi/browse/category.jsp?id=1003",
    # "DIA": "https://diaonline.supermercadosdia.com.ar/category/Despensa",
    # "Carrefour": "https://www.carrefour.com.ar/despensa"
}

def scrape_coto(url):
    productos = []
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    cards = soup.find_all('div', class_='producto')

    for card in cards:
        nombre_tag = card.find('div', class_='descrip_full')
        precio_tag = card.find('span', class_='atg_store_newPrice')
        link_tag = card.find('a', href=True)

        nombre = nombre_tag.text.strip() if nombre_tag else 'Nombre no disponible'
        precio = precio_tag.text.strip().replace('$', '').replace('.', '') if precio_tag else 'Precio no disponible'
        url_producto = urljoin("https://www.cotodigital3.com.ar", link_tag['href']) if link_tag else 'URL no disponible'

        productos.append(['COTO', nombre, precio, url_producto])

    return productos

# Ejecutamos el script y guardamos en CSV
data = []
data.extend(scrape_coto(supermercados["COTO"]))
# time.sleep(2)
# data.extend(scrape_dia(supermercados["DIA"]))
# time.sleep(2)
# data.extend(scrape_carrefour(supermercados["Carrefour"]))

# Guardamos los datos
columns = ["Supermercado", "Producto", "Precio", "URL"]
df = pd.DataFrame(data, columns=columns)
df.to_csv("productos_supermercados.csv", index=False)
print("Extracción completada y guardada en productos_supermercados.csv")
