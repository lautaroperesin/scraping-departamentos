import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class SarricchioScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Sarricchio ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Sarricchio")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select using reported classes
            cards = soup.select('.property_container')
            # If empty, try fallback to generic items
            if not cards:
                 cards = soup.select('.property_item')

            for card in cards:
                try:
                    # Title
                    title_tag = card.select_one('.property_title_link')
                    if not title_tag:
                         title_tag = card.select_one('a.title')
                    if not title_tag:
                         continue

                    titulo = title_tag.text.strip()
                    
                    # Link
                    link = title_tag['href']
                    if not link.startswith('http'):
                         link = f"https://sarricchio.com{link}"

                    # Price
                    price_tag = card.select_one('.price_container')
                    if not price_tag:
                         price_tag = card.select_one('.price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # ID
                    # URL: index.php?option=com_siiweb&view=property&id=880&Itemid=101
                    # Extract 'id' param
                    try:
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(link)
                        id_publicacion = parse_qs(parsed.query).get('id', [None])[0]
                        if not id_publicacion:
                             id_publicacion = link[-10:]
                    except:
                        id_publicacion = link[-10:]

                    # Description
                    # Sometimes location is in .location
                    loc_tag = card.select_one('.location')
                    descripcion = loc_tag.text.strip() if loc_tag else titulo

                    resultados_normalizados.append({
                        'id': f"SARRICCHIO_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Sarricchio Inmobiliaria'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Sarricchio: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Sarricchio: {e}")

        return resultados_normalizados
