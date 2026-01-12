import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class RaffinScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Raffin ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # Tokko/Gimenez pattern often needs a browser-like UA
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Raffin")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            cards = soup.select('.thumbnail_one')

            for card in cards:
                try:
                    # Title
                    title_tag = card.select_one('.thum_title h5 a')
                    if not title_tag:
                        continue
                    titulo = title_tag.get('title', title_tag.text.strip())
                    
                    # Link
                    link = title_tag['href']
                    
                    # ID extraction
                    id_tag = card.select_one('.thum_title h7')
                    if id_tag:
                        id_text = id_tag.text.strip() # "Código: 12345"
                        id_publicacion = id_text.replace('Código:', '').strip()
                    else:
                        id_publicacion = link.split('/')[-1]

                    # Price
                    price_tag = card.select_one('.area_price .sale')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # Description
                    description_tag = card.select_one('.thum_title p')
                    descripcion = description_tag.text.strip() if description_tag else ""
                    
                    resultados_normalizados.append({
                        'id': f"RAFFIN_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Raffin Inmobiliaria'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Raffin: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Raffin: {e}")

        return resultados_normalizados
