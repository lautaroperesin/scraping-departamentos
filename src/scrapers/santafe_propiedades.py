import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class SantaFePropiedadesScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Santa Fe Propiedades ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con SF Propiedades")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Selectors based on inspection
            # Looking for containers with class 'propiedad-index' or similar
            cards = soup.select('.propiedad-index')
            # Fallback
            if not cards:
                 # Try finding elements that contain specific button text
                 cards = [el.parent for el in soup.find_all(string="ver detalles")]

            for card in cards:
                try:
                    if not card: continue
                    
                    # Title (h3 or h4 or first strong)
                    title_tag = card.find(['h3', 'h4'])
                    if not title_tag:
                         title_tag = card.find('strong')
                    
                    titulo = title_tag.text.strip() if title_tag else "Sin título"
                    
                    # Link
                    link_tag = card.find('a', href=lambda x: x and 'descripcion.php' in x)
                    if not link_tag:
                         continue
                         
                    link = link_tag['href']
                    if not link.startswith('http'):
                         link = f"https://www.santafe-propiedades.com.ar/{link}"

                    # Price
                    price_tag = card.select_one('.precio')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # ID
                    # descripcion.php?id=203...
                    try:
                        from urllib.parse import urlparse, parse_qs
                        parsed = urlparse(link)
                        id_publicacion = parse_qs(parsed.query).get('id', [None])[0]
                        if not id_publicacion:
                             id_publicacion = link.split('=')[-1]
                    except:
                        id_publicacion = link[-10:]

                    # Description
                    # Usually just the title contains info, or maybe an address div
                    text_content = card.get_text(" ", strip=True)
                    descripcion = text_content[:100] # Use snippet as description if no specific tag

                    resultados_normalizados.append({
                        'id': f"SFPROP_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Santa Fe Propiedades'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta SF Prop: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando SF Prop: {e}")

        return resultados_normalizados
