import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
import re

class UretacortesScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Ureta Cortes ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # Using browser User-Agent
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Ureta Cortes")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Based on inspection, items are likely in col-md-9 inside a row
            # But let's look for common property classes or just the structure containing 'h4 a'
            
            # The structure for Ureta seems to be a list of divs in a .row in .col-md-9
            # Since we don't have a unique class for the card, let's iterate over typical containers or find by title tag
            
            # Try to find all h4 links which seemed to be the titles
            title_links = soup.select('h4 a')
            
            # We will traverse up from title links to find the "card" container
            processed_links = set()

            for link_tag in title_links:
                try:
                    href = link_tag['href']
                    if href in processed_links:
                        continue
                    processed_links.add(href)

                    # Title
                    titulo = link_tag.text.strip()
                    
                    # Link
                    link = href

                    # Container: The parent of h4, usually a div or the h4 itself is inside the card
                    # Let's assume the hierarchy is roughly div.card > div.body > h4 > a
                    # We can search for price in the siblings or parent
                    
                    # Go up to find a container that has text content
                    card = link_tag.find_parent('div', class_='row') # Maybe a row per item?
                    if not card:
                         card = link_tag.find_parent('div', class_='col-sm-6') # Grid item?
                    if not card:
                         # Fallback: look at immediate parent's parent
                         card = link_tag.parent.parent

                    # Price
                    # Search for price pattern in the card text
                    # Pattern: $ 123.456
                    card_text = card.get_text(" ", strip=True) if card else ""
                    price_match = re.search(r'\$\s*[\d\.,]+', card_text)
                    precio = price_match.group(0) if price_match else "Consultar"

                    # ID
                    # Extract from link if possible /propiedad/ID/
                    # or look for wp post id class
                    id_publicacion = link.strip('/').split('/')[-1]
                    if not id_publicacion or id_publicacion.startswith('?'):
                         # Try previous segment
                         parts = link.strip('/').split('/')
                         if len(parts) > 1: s = parts[-2]
                         id_publicacion = s if s else "unknown_" + titulo[:10]

                    # Description
                    descripcion = titulo # Default to title as it usually contains info

                    resultados_normalizados.append({
                        'id': f"URETACORTES_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Ureta Cortes Inmobiliaria'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Ureta Cortes: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Ureta Cortes: {e}")

        return resultados_normalizados
