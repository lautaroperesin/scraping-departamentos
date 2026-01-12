import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class AlicandroScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Alicandro ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Alicandro")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select property cards using the Christen/Tokko pattern
            cards = soup.select('.resultados-list li')
            
            for card in cards:
                try:
                    # ID
                    prop_id = card.get('prop-id')
                    if not prop_id:
                         # Fallback to finding .codref
                        codref = card.select_one('.codref')
                        if codref:
                             prop_id = codref.text.strip().replace('Ref:', '').strip()
                        else:
                             continue
                    
                    # Title
                    title_elem = card.select_one('.prop-desc-tipo-ub')
                    titulo = title_elem.text.strip() if title_elem else "Sin título"
                    
                    # Location
                    loc_elem = card.select_one('.prop-desc-dir')
                    ubicacion = loc_elem.text.strip() if loc_elem else ""
                    
                    # Price
                    price_elem = card.select_one('.prop-valor-nro')
                    precio = price_elem.get_text(strip=True) if price_elem else "Consultar"
                        
                    # Link
                    link_elem = card.find('a')
                    link = self.url_base
                    if link_elem and link_elem.get('href'):
                        link = link_elem['href']
                        if not link.startswith('http'):
                            link = f"https://www.alicandro.com.ar{link}"

                    resultados_normalizados.append({
                        'id': f"ALICANDRO_{prop_id}",
                        'titulo': titulo,
                        'descripcion': ubicacion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Alicandro Inmobiliaria'
                    })
                    
                except Exception as e:
                    print(f"Error parseando tarjeta Alicandro: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scrapeando Alicandro: {e}")
            
        return resultados_normalizados
