import requests
import json
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class RemaxScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Remax ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Remax")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # La data está en un script tag con id "ng-state" en formato JSON
            script_tag = soup.find('script', id='ng-state')
            if not script_tag:
                print("No se encontró el script de estado de Remax (ng-state)")
                return []
                
            json_content = script_tag.string
            try:
                data_json = json.loads(json_content)
            except json.JSONDecodeError:
                print("Error al decodificar JSON de Remax")
                return []
            
            # El JSON tiene claves numéricas dinámicas. Buscamos la que tiene los 'listings'.
            # Estructura: { KEY: { 'b': { 'data': { 'data': [ ... ] } } } }
            
            listings = []
            for key, value in data_json.items():
                try:
                    # Navegamos la estructura para encontrar la lista de datos
                    possible_data = value.get('b', {}).get('data', {}).get('data', [])
                    if isinstance(possible_data, list) and len(possible_data) > 0:
                        # Verificamos si parece ser una propiedad (tiene precio o título)
                        first_item = possible_data[0]
                        if 'price' in first_item or 'listingStatus' in first_item:
                            listings = possible_data
                            break
                except AttributeError:
                    continue
            
            if not listings:
                print("No se encontraron listados en la estructura JSON de Remax")
                # Fallback: intentar imprimir las claves para debug (opcional, solo print)
                # print(f"Claves encontradas: {data_json.keys()}")
                return []

            for prop in listings:
                try:
                    titulo = prop.get('title', 'Sin título')
                    slug = prop.get('slug', '')
                    link = f"https://www.remax.com.ar/listings/{slug}" if slug else self.url_base
                    
                    descripcion = prop.get('displayAddress', '')
                    id_remax = prop.get('id', '')
                    
                    price_val = prop.get('price', 0)
                    currency_data = prop.get('currency', {})
                    moneda = currency_data.get('value', '$')
                    
                    precio = f"{moneda} {price_val}"
                    
                    resultados_normalizados.append({
                        'id': f"REMAX_{id_remax}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Remax'
                    })

                except Exception as e:
                    print(f"Error parseando propiedad Remax: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Remax: {e}")

        return resultados_normalizados