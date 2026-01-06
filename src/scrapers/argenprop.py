from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

class ArgenpropScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Argenprop ({self.url_base})...")
        resultados_normalizados = []
        
        # Check for price limit in URL
        max_price = None
        match = re.search(r'pesos-hasta-(\d+)', self.url_base)
        if match:
             max_price = int(match.group(1))
             print(f"Filtro de precio detectado: hasta ${max_price}")
        
        # Max loop safety
        max_pages = 5
        
        for page in range(1, max_pages + 1):
            
            # Construct URL for specific page
            if page == 1:
                current_url = self.url_base
            else:
                # Add or update pagina-{n} in query params
                parsed = urllib.parse.urlparse(self.url_base)
                # Keep existing query parts, but filter out any existing pagina-X
                # We need to manually handle this split because parse_qs gives dictionary
                # and "pagina-2" is a key with no value.
                
                query_parts = parsed.query.split('&')
                new_query_parts = [p for p in query_parts if not p.startswith('pagina-') and p]
                
                # Add the new page param
                new_query_parts.insert(0, f"pagina-{page}")
                
                new_query = '&'.join(new_query_parts)
                current_url = urllib.parse.urlunparse(parsed._replace(query=new_query))

            print(f"Scraping Argenprop pagina {page}: {current_url}")

            try:
                # Argenprop often blocks requests without a valid User-Agent
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'es-ES,es;q=0.9'
                }
                
                response = requests.get(current_url, headers=headers, timeout=15)
                
                if response.status_code != 200:
                    print(f"Error {response.status_code} al conectar con Argenprop pagina {page}")
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Tarjetas de propiedad
                cards = soup.select('.listing__item')
                
                if not cards:
                    print(f"No se encontraron propiedades en pagina {page}. Finalizando.")
                    break
                
                count_in_page = 0

                for card_div in cards:
                    try:
                        # El elemento <a> dentro del div tiene mucha data
                        link_tag = card_div.find('a', class_='card')
                        if not link_tag:
                            continue
                            
                        # ID
                        # data-item-card="18760378" en el <a> o id="18760378" en el <div>
                        id_argenprop = card_div.get('id')
                        if not id_argenprop and link_tag.has_attr('data-item-card'):
                            id_argenprop = link_tag['data-item-card']
                        
                        if not id_argenprop:
                            continue # Skip if no ID

                        # Título
                        title_tag = link_tag.find(['h2', 'p'], class_='card__title')
                        titulo = title_tag.text.strip() if title_tag else "Sin Título"
                        
                        # Descripción / Dirección
                        address_tag = link_tag.find(['h2', 'p'], class_='card__address') 
                        if not address_tag:
                             address_tag = link_tag.select_one('.card__address')
                        
                        descripcion = address_tag.text.strip() if address_tag else titulo

                        # Precio
                        price_tag = link_tag.select_one('.card__price')
                        if price_tag:
                             raw_price = price_tag.text.strip()
                             # Limpiar precio (e.g., "$ 700.000 + $ 90.000 expensas")
                             # Nos quedamos con la primera parte
                             precio = raw_price.split('+')[0].strip()
                             # Normalizar espacios
                             precio = " ".join(precio.split())
                             
                             # Filtering logic checks against max_price if set
                             if max_price:
                                 try:
                                     clean_val_str = precio.replace('$','').replace('.','').replace(' ','')
                                     # check if it is numeric
                                     if clean_val_str.isdigit():
                                         val = int(clean_val_str)
                                         if val > max_price:
                                             # print(f"Skipping {titulo} - {precio} > {max_price}")
                                             continue
                                     # If it's USD, and our filter is pesos-hasta-X, we might want to exclude it too
                                     # but the user didn't explicitly say "exclude USD", though they said "filtraste mal (mas de 750k)"
                                     # If we see USD, we might be safe to keep or filtering logic is ambiguous.
                                     # Usually 'pesos-hasta' implies extracting items in pesos.
                                     if "USD" in precio:
                                          pass # Decide policy? For now, keep unless it's clearly expensive in number?
                                          # Actually, filtering out USD if we want pesos might be desired.
                                          # The 'solo-ver-pesos' arg suggests we only want Pesos.
                                          # Argenprop sometimes ignores it.
                                          # Let's filter USD if 'pesos-hasta' is present.
                                          if 'pesos' in self.url_base:
                                              continue

                                 except:
                                     pass
                        else:
                             precio = "Consultar"

                        # Link
                        href = link_tag['href']
                        base_domain = "https://www.argenprop.com"
                        link = urllib.parse.urljoin(base_domain, href)

                        res_dict = {
                            'id': f"ARGENPROP_{id_argenprop}",
                            'titulo': titulo,
                            'descripcion': descripcion,
                            'precio': precio,
                            'link': link,
                            'portal': 'Argenprop'
                        }
                        
                        if not any(r['id'] == res_dict['id'] for r in resultados_normalizados):
                            resultados_normalizados.append(res_dict)
                            count_in_page += 1

                    except Exception as e:
                        print(f"Error parseando tarjeta Argenprop: {e}")
                        continue
                
                print(f"Encontrados {count_in_page} nuevos resultados en pagina {page}")

            except Exception as e:
                print(f"Error scrapeando Argenprop pagina {page}: {e}")
                
        return resultados_normalizados
