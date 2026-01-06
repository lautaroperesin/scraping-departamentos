import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
import re

class EsquivelScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Esquivel ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Esquivel")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Selector for property cards based on browser analysis
            cards = soup.select('.product-item')

            for card in cards:
                try:
                    # Title: Property Type
                    title_tag = card.select_one('.propiedad-tipo span')
                    tipo_propiedad = title_tag.text.strip() if title_tag else "Departamento"
                    
                    # Link
                    link_tag = card.select_one('a[href^="propiedad.php"]')
                    if not link_tag:
                        continue
                    link = link_tag['href']
                    if not link.startswith('http'):
                        link = f"https://www.esquivelinmobiliaria.com.ar/{link}"
                        
                    # ID from Link
                    # link is usually property.php?id=414
                    try:
                        id_match = re.search(r'id=(\d+)', link)
                        if id_match:
                            prop_id = id_match.group(1)
                        else:
                            prop_id = link[-10:]
                    except:
                        prop_id = "UNKNOWN"

                    # Location/Address (Description)
                    location_tag = card.select_one('.propiedad-detalle p')
                    # format is: <span class...></span>&nbsp;&nbsp;Area<br>Address
                    # We can get text and clean it
                    if location_tag:
                        full_text = location_tag.get_text(" ", strip=True)
                        descripcion = full_text
                        ubicacion = full_text
                    else:
                        descripcion = ""
                        ubicacion = ""
                    
                    # Construct a better title like "Departamento en [Location]"
                    titulo = f"{tipo_propiedad} en {ubicacion}"

                    # Price - Not available in list view, so default to Consultar
                    # We could try to fetch detail page but that's expensive and not requested yet.
                    precio = "Consultar"
                    
                    resultados_normalizados.append({
                        'id': f"ESQUIVEL_{prop_id}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'ubicacion': ubicacion,
                        'link': link,
                        'portal': 'Esquivel Inmobiliaria'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Esquivel: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Esquivel: {e}")

        return resultados_normalizados
