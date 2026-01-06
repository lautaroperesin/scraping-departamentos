import requests
import json
import re
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
import html

class BottaiScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Bottai ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Bottai")
                return []

            # Método 1: Intentar extraer JSON del script (más limpio)
            # Buscamos: var inmuebles = [...];
            pattern = r'var inmuebles = (\[.*?\]);'
            match = re.search(pattern, response.text, re.DOTALL)
            
            if match:
                try:
                    json_str = match.group(1)
                    inmuebles = json.loads(json_str)
                    
                    for inm in inmuebles:
                        id_inm = inm.get('id')
                        titulo = inm.get('titulo', 'Sin título')
                        # Limpiar entidades HTML de la descripción y título
                        titulo = html.unescape(titulo)
                        descripcion = html.unescape(inm.get('descripcion', ''))
                        precio = inm.get('precio', 'Consultar')
                        
                        link = f"https://www.bottai.com.ar/inmueble_{id_inm}"
                        
                        resultados_normalizados.append({
                            'id': f"BOTTAI_{id_inm}",
                            'titulo': titulo,
                            'descripcion': descripcion,
                            'precio': precio,
                            'link': link,
                            'portal': 'Bottai'
                        })
                    
                    return resultados_normalizados
                    
                except Exception as e:
                    print(f"Error parseando JSON de Bottai: {e}, intentando HTML...")
            
            # Método 2: Fallback a parsing HTML si falla el regex o no hay JSON
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.select('.col-xs-12.col-sm-12 .media.thumbnail')
            
            for card in cards:
                try:
                    title_tag = card.select_one('.caption h4 a')
                    if not title_tag:
                        continue
                        
                    titulo = title_tag.text.strip()
                    href = title_tag['href'] # Ej: inmueble_5709
                    
                    # ID
                    id_bottai = href.replace('inmueble_', '')
                    link = f"https://www.bottai.com.ar/{href}"
                    
                    # Precio
                    price_tag = card.select_one('.thumbnail-price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"
                    
                    # Descripcion
                    desc_tag = card.select_one('.caption p')
                    descripcion = desc_tag.text.strip() if desc_tag else ""
                    
                    resultados_normalizados.append({
                        'id': f"BOTTAI_{id_bottai}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Bottai'
                    })
                    
                except Exception as e:
                    print(f"Error parseando tarjeta Bottai: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Bottai: {e}")

        return resultados_normalizados
