import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class SalasScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Salas ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Salas")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las tarjetas de los productos
            cards = soup.select('#posts .entry')

            for card in cards:
                try:
                    # Titulo
                    title_tag = card.select_one('.real-estate-item-price h3')
                    if not title_tag:
                        continue
                    titulo = title_tag.text.strip()
                    
                    # Link
                    link_tag = card.select_one('.real-estate-item-image a')
                    if not link_tag:
                        continue
                    link = link_tag['href']
                    
                    # ID extraction: .../propiedad/4487-guemes-3800.html -> 4487
                    try:
                        # Obtenemos la parte final: 4487-guemes-3800.html
                        slug = link.split('/')[-1]
                        # Tomamos lo que esta antes del primer guion
                        id_publicacion = slug.split('-')[0]
                    except:
                        id_publicacion = link[-10:] # Fallback

                    # Precio
                    price_tag = card.select_one('.real-estate-item-desc .thumb-icono-2 span')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # Descripcion
                    description_tag = card.select_one('.real-estate-item-desc .thumb-icono-2')
                    descripcion = description_tag.text.strip() if description_tag else ""
                    
                    resultados_normalizados.append({
                        'id': f"SALAS_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Salas Inmobiliaria'
                    })

                except Exception as e:
                    # Si falla una tarjeta, la saltamos pero seguimos con las otras
                    print(f"Error parseando tarjeta: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Salas: {e}")

        return resultados_normalizados
