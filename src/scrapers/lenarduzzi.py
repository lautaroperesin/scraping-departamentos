import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class LenarduzziScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Lenarduzzi ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # Houzez theme usually loads via standard HTML
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Lenarduzzi")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Houzez item wrap
            cards = soup.select('.item-wrap')

            for card in cards:
                try:
                    # ID
                    id_publicacion = card.get('data-propid')
                    if not id_publicacion:
                         continue

                    # Title
                    title_tag = card.select_one('.item-title a')
                    if not title_tag:
                        continue
                    titulo = title_tag.text.strip()
                    
                    # Link
                    link = title_tag['href']

                    # Price
                    price_tag = card.select_one('.item-price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # Description/Address
                    # Houzez often puts address in <address class="item-address">
                    address_tag = card.select_one('address.item-address')
                    descripcion = address_tag.text.strip() if address_tag else ""
                    
                    # Append other details if available
                    amenities = card.select('.item-amenities span')
                    if amenities:
                        amenity_texts = [a.text.strip() for a in amenities if a.text.strip()]
                        if amenity_texts:
                            descripcion += " | " + " - ".join(amenity_texts)

                    resultados_normalizados.append({
                        'id': f"LENARDUZZI_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Lenarduzzi Inmobiliaria'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Lenarduzzi: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Lenarduzzi: {e}")

        return resultados_normalizados
