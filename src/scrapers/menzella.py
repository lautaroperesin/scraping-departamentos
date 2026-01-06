from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import urllib.parse

class MenzellaScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Menzella ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Menzella")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tarjetas de propiedad
            cards = soup.select('.items1__item')

            for card in cards:
                try:
                    # Título y Link
                    title_tag = card.select_one('.items1__title')
                    if not title_tag:
                        continue
                        
                    titulo = title_tag.text.strip()
                    # El href es relativo y tiene parametros: ?idprop=58031&...
                    href = title_tag['href']
                    base_domain = "https://www.menzellainmobiliaria.com.ar/"
                    link = urllib.parse.urljoin(base_domain, href)

                    # ID
                    # Opción 1: data-idprop en el corazón
                    heart_icon = card.select_one('.items1__heart')
                    if heart_icon and heart_icon.has_attr('data-idprop'):
                        id_menzella = heart_icon['data-idprop']
                    else:
                        # Opción 2: Parse from URL or Code
                        # items1__code: COD. 65030 -> Esto parece ser un código interno visible, no necesariamente el ID técnico
                        # Preferimos el ID técnico de la URL
                        parsed_url = urllib.parse.urlparse(link)
                        query_params = urllib.parse.parse_qs(parsed_url.query)
                        id_menzella = query_params.get('idprop', [''])[0]
                        
                        if not id_menzella:
                            # Fallback al código visible
                            code_tag = card.select_one('.items1__code')
                            if code_tag:
                                id_menzella = code_tag.text.replace('COD.', '').strip()
                            else:
                                id_menzella = "UNKNOWN_" + titulo[:10]

                    # Precio
                    price_tag = card.select_one('.items1__price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"
                    # Limpieza básica de precio (quitar /mes si se quiere, o dejarlo)
                    # precio = precio.replace('/mes', '').strip()

                    # Descripción / Ubicación
                    location_tag = card.select_one('.items1__location')
                    descripcion = location_tag.text.strip() if location_tag else ""

                    resultados_normalizados.append({
                        'id': f"MENZELLA_{id_menzella}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Menzella'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Menzella: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Menzella: {e}")

        return resultados_normalizados
