import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class PinoMaglioneScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Pino Maglione ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Pino Maglione")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Select property cards
            cards = soup.select('.resultados-list li')
            
            for card in cards:
                try:
                    # ID
                    # Try to get from .codref
                    id_tag = card.select_one('.codref')
                    if id_tag:
                         prop_id = id_tag.text.strip().replace('Ref:', '').strip()
                    else:
                         # Fallback to finding ID in inner text or similar pattern
                         text = card.get_text()
                         import re
                         match = re.search(r'PAP\d+', text)
                         if match:
                             prop_id = match.group(0)
                         else:
                             continue
                    
                    # Title
                    # Often in .prop-desc-tipo-ub (Type + Location)
                    # or just .prop-desc
                    title_elem = card.select_one('.prop-desc')
                    titulo = title_elem.text.strip().replace('\n', ' ') if title_elem else "Sin título"
                    
                    # Price
                    price_elem = card.select_one('.prop-valor-nro')
                    if price_elem:
                        # Price element often has child elements (like the ID div). Get direct text if possible
                        # or just get all text and split. Usually price is first.
                        # We can use .contents[0] if it's a text node
                        precio = price_elem.contents[0].strip() if price_elem.contents else price_elem.get_text(strip=True)
                        if not '$' in precio and not 'USD' in precio:
                            # Try to find the price text node specifically
                            precio = [t for t in price_elem.stripped_strings if '$' in t or 'USD' in t]
                            precio = precio[0] if precio else "Consultar"
                    else:
                        precio = "Consultar"

                    # Description (Address)
                    # Usually in .prop-desc-dir
                    loc_elem = card.select_one('.prop-desc-dir')
                    descripcion = loc_elem.text.strip() if loc_elem else titulo

                    # Link
                    link_elem = card.find('a')
                    link = link_elem['href'] if link_elem else self.url_base
                    if not link.startswith('http'):
                        link = f"https://www.pinomaglione.com.ar{link}"

                    resultados_normalizados.append({
                        'id': f"PINOMAGLIONE_{prop_id}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Pino Maglione'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Pino Maglione: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Pino Maglione: {e}")

        return resultados_normalizados
