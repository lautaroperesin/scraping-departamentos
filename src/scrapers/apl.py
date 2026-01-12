import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class AplScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en APL Inmobiliaria ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # APL likely uses cookies or specific headers, but let's try standard first
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con APL")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select relevant cards. Based on inspection:
            # Often .card or .property-item. Let's select all cards that have a link to 'propiedades'
            # to be safe about the structure.
            cards = soup.select('.card')

            for card in cards:
                try:
                    # Title (usually h5 in card-body)
                    title_tag = card.select_one('.card-body h5')
                    if not title_tag:
                         # Fallback
                         title_tag = card.select_one('h5')
                    
                    if not title_tag:
                         continue

                    titulo = title_tag.text.strip()
                    
                    # Link
                    link_tag = card.select_one('a')
                    link = self.url_base
                    if link_tag and link_tag.get('href'):
                         link = link_tag['href']
                         if not link.startswith('http'):
                              link = f"https://www.aplinmobiliaria.com{link}"
                    
                    # Price
                    # Usually in card-footer or a separate price div
                    price_tag = card.select_one('.price')
                    if not price_tag:
                        price_tag = card.select_one('.card-footer')
                    
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # ID - Extract from URL
                    # /propiedades/LAS-HERAS-66471669988915307
                    try:
                        id_publicacion = link.split('/')[-1]
                    except:
                        id_publicacion = link[-20:]

                    # Description
                    # Often the title is the description, or there is an address line
                    descripcion = titulo 

                    resultados_normalizados.append({
                        'id': f"APL_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'APL Inmobiliaria'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta APL: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando APL: {e}")

        return resultados_normalizados
