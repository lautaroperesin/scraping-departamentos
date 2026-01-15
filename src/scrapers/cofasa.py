import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class CofasaScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Cofasa ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Cofasa")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select property cards
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
                             # Try to get from link
                             link_elem = card.find('a')
                             if link_elem:
                                 href = link_elem.get('href', '')
                                 parts = href.split('-')
                                 if parts and parts[-1].isdigit():
                                     prop_id = parts[-1]
                    
                    if not prop_id:
                        continue
                    
                    # Title (Type + Location)
                    title_elem = card.select_one('.prop-desc-tipo-ub')
                    titulo = title_elem.text.strip() if title_elem else "Sin título"
                    
                    # Location (Address)
                    loc_elem = card.select_one('.prop-desc-dir')
                    ubicacion = loc_elem.text.strip() if loc_elem else ""
                    
                    # Price
                    price_elem = card.select_one('.prop-valor-nro')
                    if price_elem:
                        # Sometimes price element contains other tags, get text only
                        precio = price_elem.get_text(strip=True)
                    else:
                        precio = "Consultar"
                        
                    # Link
                    link_elem = card.find('a')
                    link = self.url_base
                    if link_elem and link_elem.get('href'):
                        link = link_elem['href']
                        if not link.startswith('http'):
                            link = f"https://www.cofasainmobiliaria.com.ar{link}"

                    resultados_normalizados.append({
                        'id': f"COFASA_{prop_id}",
                        'titulo': titulo,
                        'descripcion': ubicacion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Cofasa Inmobiliaria'
                    })
                    
                except Exception as e:
                    print(f"Error parseando tarjeta Cofasa: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scrapeando Cofasa: {e}")
            
        return resultados_normalizados
