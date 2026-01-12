import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class PenalvaScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Penalva ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # Penalva blocks simple requests sometimes, let's use a standard User-Agent
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Penalva")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            cards = soup.select('article.property-item')

            for card in cards:
                try:
                    # Title and Link
                    title_tag = card.select_one('h4 a')
                    if not title_tag:
                        continue
                        
                    titulo = title_tag.text.strip()
                    link = title_tag['href']

                    # Description
                    # Buscamos en div.detail p
                    description_tag = card.select_one('div.detail p')
                    descripcion = description_tag.text.strip() if description_tag else ""
                    
                    # Also append address if available separately using selectors found or just rely on title as it contains address
                    # The browser agent said title often has address. Let's stick to title + detail.

                    # Price
                    price_tag = card.select_one('h5.price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # ID
                    # Extract from URL slug
                    # https://penalvainmobiliaria.com.ar/property/slug/
                    try:
                        id_publicacion = link.strip('/').split('/')[-1]
                    except:
                        id_publicacion = link[-20:] # fallback

                    resultados_normalizados.append({
                        'id': f"PENALVA_{id_publicacion}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Penalva'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Penalva: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Penalva: {e}")

        return resultados_normalizados
