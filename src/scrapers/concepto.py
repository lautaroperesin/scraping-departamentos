import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class ConceptoScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Concepto ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # Concepto is Tokko based, likely needs User-Agent
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Concepto")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Selectors for Concepto (Tokko)
            cards = soup.select('.item-propiedad')
            if not cards:
                 cards = soup.select('.property-item') # Generic Tokko fallback
                 
            for card in cards:
                try:
                    # Title
                    title_tag = card.select_one('h4')
                    if not title_tag:
                         title_tag = card.select_one('.property-title')
                    
                    titulo = title_tag.text.strip() if title_tag else "Sin título"
                    
                    # Link
                    link_tag = card.select_one('a')
                    link = link_tag['href']
                    if not link.startswith('http'):
                         link = f"https://www.conceptonegociosinmobiliarios.com.ar{link}"

                    # Price
                    price_tag = card.select_one('.p_precio')
                    if not price_tag:
                         price_tag = card.select_one('.property-price')
                    
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # ID
                    # Often in card text or URL
                    # Let's try finding the reference code in text
                    # "Ref: CAP123"
                    text = card.get_text()
                    import re
                    match = re.search(r'(CAP\d+|Ref:\s*\w+)', text)
                    if match:
                         id_publicacion = match.group(0).replace('Ref:', '').strip()
                    else:
                         id_publicacion = link.split('/')[-1]

                    # Description
                    # Address or description text
                    desc_tag = card.select_one('.p_direccion')
                    descripcion = desc_tag.text.strip() if desc_tag else titulo

                    resultados_normalizados.append({
                        'id': f"CONCEPTO_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Concepto Inmobiliaria'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Concepto: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Concepto: {e}")

        return resultados_normalizados
