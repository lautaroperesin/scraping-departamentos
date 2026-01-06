import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class ChristenScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Christen ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # Add user agent headers to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select property cards using the selector found
            cards = soup.select('.resultados-list li')
            
            for card in cards:
                try:
                    # ID
                    prop_id = card.get('prop-id')
                    if not prop_id:
                        continue
                    
                    # Title (Type + Location)
                    title_elem = card.select_one('.prop-desc-tipo-ub')
                    titulo = title_elem.text.strip() if title_elem else "Sin título"
                    
                    # Location (Address)
                    loc_elem = card.select_one('.prop-desc-dir')
                    ubicacion = loc_elem.text.strip() if loc_elem else "Sin ubicación"
                    
                    # Price
                    price_elem = card.select_one('.prop-valor-nro')
                    if price_elem:
                        # The text might be like "$680.000\n CAP..."
                        # We try to get just the first part which is usually the price
                        raw_text = price_elem.get_text(strip=True)
                        # A simple heuristic to extract the price part: take split by '$' if needed or just use raw
                        # Usually the structure is <div class="prop-valor-nro"> $680.000 <div class="codref">...</div></div>
                        # get_text might strip newlines, so "$680.000CAP7645956"
                        # It is safer to inspect children or just take the first text node.
                        # Let's try finding the text node directly or splitting.
                        
                        # Alternative: iterate over contents
                        precio_parts = [str(x).strip() for x in price_elem.contents if isinstance(x, str) and x.strip()]
                        if precio_parts:
                            precio = [p for p in precio_parts if '$' in p or p.replace('.', '').isdigit()]
                            precio = precio[0] if precio else raw_text
                        else:
                            precio = raw_text
                    else:
                        precio = "Consultar"
                        
                    # Link
                    link_elem = card.find('a')
                    if link_elem and link_elem.get('href'):
                        link = link_elem['href']
                        if not link.startswith('http'):
                            link = f"https://www.christen.com.ar{link}"
                    else:
                        link = self.url_base

                    resultados_normalizados.append({
                        'id': f"CHRISTEN_{prop_id}",
                        'titulo': titulo,
                        'descripcion': ubicacion, # Mapping Address to Description
                        'precio': precio,
                        'ubicacion': ubicacion,
                        'link': link,
                        'portal': 'Christen Inmobiliaria'
                    })
                    
                except Exception as e:
                    print(f"Error parseando tarjeta Christen: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scrapeando Christen: {e}")
            
        return resultados_normalizados
