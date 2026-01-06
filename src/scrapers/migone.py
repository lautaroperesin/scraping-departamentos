from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

class MigoneScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Migone ({self.url_base})...")
        resultados_normalizados = []
        page = 0
        max_pages = 5 # Safety limit to avoid infinite loops during testing
        
        while page < max_pages:
            # Construct URL with current page
            # The base url usually has p=0, we need to replace or update it.
            parsed_url = urllib.parse.urlparse(self.url_base)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            query_params['p'] = [str(page)]
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            current_url = urllib.parse.urlunparse(parsed_url._replace(query=new_query))
            
            print(f"Scraping page {page}: {current_url}")
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                
                response = requests.get(current_url, headers=headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"Error {response.status_code} al conectar con Migone en pagina {page}")
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Logic derived from analysis: Find .price elements and look at their parents
                # Or try to find a container that holds repeated items.
                # Based on analysis, let's try finding all containers that might be cards.
                # The analysis showed links like 'departamento-en-venta...' inside the parent of .price
                
                price_elements = soup.select('.price')
                
                if not price_elements:
                    print("No se encontraron propiedades en esta página. Finalizando.")
                    break
                
                prop_count_in_page = 0
                
                # We iterate over unique parents of price elements to avoid duplicates if multiple price tags exist per card
                cards = []
                seen_cards = set()
                
                for price_el in price_elements:
                    # Attempt to find the card container.
                    # Usually it's a few levels up.
                    # We can look for a div that has 'item' or 'col' class
                    card = price_el.find_parent('div', class_=lambda x: x and ('item' in x or 'col' in x or 'property' in x))
                    
                    if not card:
                        # Fallback: go up 3 levels
                        card = price_el.parent.parent.parent
                    
                    if card and card not in seen_cards:
                        cards.append(card)
                        seen_cards.add(card)

                for card in cards:
                    try:
                        # Link and Title
                        # Usually inside an <a> tag
                        link_tag = card.find('a', href=True)
                        if not link_tag:
                            continue
                        
                        href = link_tag['href']
                        if 'javascript' in href or '#' == href:
                            continue

                        base_domain = "https://www.migoneinmobiliaria.com.ar/"
                        link = urllib.parse.urljoin(base_domain, href)
                        
                        # Title defaults to text of the link or some header
                        title_tag = card.find(['h3', 'h4', 'h2'])
                        if title_tag:
                            titulo = title_tag.text.strip()
                        else:
                            # Use part of the link text or link itself
                            titulo = link_tag.text.strip()
                            if not titulo:
                                # Try to parse title from slug
                                slug = href.strip('/').split('/')[-1]
                                titulo = slug.replace('-', ' ').title()

                        # ID
                        # Extract from slug: ...-ficha-mig4998 -> mig4998
                        # Or query param cod= if exists
                        slug = link.strip('/').split('/')[-1]
                        if 'ficha-' in slug:
                             id_migone = slug.split('ficha-')[-1]
                        elif 'cod=' in link:
                             parsed_link = urllib.parse.urlparse(link)
                             id_migone = urllib.parse.parse_qs(parsed_link.query).get('cod', [''])[0]
                        else:
                             id_migone = slug # Fallback

                        # Ensure unique ID prefix
                        if not id_migone:
                            id_migone = "UNKNOWN_" + titulo[:10]

                        # Price
                        # We already have price_elements, but we need the specific one for this card
                        card_price_tag = card.select_one('.price') 
                        if card_price_tag:
                            precio = card_price_tag.text.strip()
                        else:
                            precio = "Consultar"

                        # Description
                        # Look for some text paragraph
                        desc_tag = card.find('p')
                        descripcion = desc_tag.text.strip() if desc_tag else titulo

                        resultados_normalizados.append({
                            'id': f"MIGONE_{id_migone}",
                            'titulo': titulo,
                            'descripcion': descripcion,
                            'precio': precio,
                            'link': link,
                            'portal': 'Migone'
                        })
                        prop_count_in_page += 1

                    except Exception as e:
                        print(f"Error parseando tarjeta Migone: {e}")
                        continue
                
                print(f"Encontrados {prop_count_in_page} resultados en pagina {page}")
                
                 # If we found no valid properties in this page, maybe we reached the end (if headers/footers fooled us)
                if prop_count_in_page == 0:
                     break

                page += 1
                # Respectful delay
                time.sleep(1)
                
            except Exception as e:
                print(f"Error scrapeando Migone pagina {page}: {e}")
                break

        return resultados_normalizados
