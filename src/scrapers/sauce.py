import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class SauceScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Sauce ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Sauce")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select property cards
            cards = soup.select('article.property-row')

            for card in cards:
                try:
                    # Title and Link
                    title_tag = card.select_one('h3.property-row-title a')
                    if not title_tag:
                        continue
                        
                    titulo = title_tag.text.strip()
                    link = title_tag['href']

                    # Description
                    description_tag = card.select_one('.property-row-content p')
                    descripcion = description_tag.text.strip() if description_tag else ""
                    
                    # Append location to description if available
                    location_tag = card.select_one('.property-row-location')
                    if location_tag:
                         descripcion += f" - {location_tag.text.strip()}"

                    # Price
                    # Intentamos buscar .property-price2 primero, si no .property-row-price
                    price_tag = card.select_one('.property-price2')
                    if not price_tag:
                        price_tag = card.select_one('.property-row-price')
                        
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # ID
                    # Intentamos extraerlo del link, formato propXXXX
                    try:
                        # Ejemplo: /properties/candido-pujato-3200-2-prop2606/
                        id_publicacion = link.strip('/').split('-')[-1]
                        if not id_publicacion.startswith('prop'):
                             id_publicacion = link.strip('/').split('/')[-1]
                    except:
                        # Fallback simple
                        id_publicacion = link.strip('/').split('/')[-1]

                    resultados_normalizados.append({
                        'id': f"SAUCE_{id_publicacion}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Sauce'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Sauce: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Sauce: {e}")

        return resultados_normalizados
