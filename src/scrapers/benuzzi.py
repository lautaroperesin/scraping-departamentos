import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class BenuzziScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Benuzzi ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
            
            # La URL ya tiene los filtros, hacemos GET directo
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Benuzzi")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las tarjetas de los productos
            cards = soup.select('.rhea-ultra-property-card-two')

            for card in cards:
                try:
                    # Titulo y Link
                    title_tag = card.select_one('.rhea-ultra-property-card-two-title a')
                    if not title_tag:
                        continue
                        
                    titulo = title_tag.text.strip()
                    link = title_tag['href']

                    # Descripcion / Direccion
                    address_tag = card.select_one('.rhea-ultra-property-card-two-address')
                    descripcion = address_tag.text.strip() if address_tag else ""
                    
                    # ID extraction: ...cod-6994/ -> 6994
                    try:
                        # Buscamos algo tipo 'cod-6994' en la URL
                        if 'cod-' in link:
                            possible_id = link.split('cod-')[-1]
                            # Removemos trailing slash si existe
                            possible_id = possible_id.rstrip('/')
                            id_publicacion = possible_id
                        else:
                             # Fallback a hash corto si no encuentra el pattern
                            id_publicacion = link[-10:]
                    except:
                        id_publicacion = link[-10:] 

                    # Precio
                    price_tag = card.select_one('.rhea-ultra-property-card-two-price .ere-price-display')
                    precio = price_tag.text.strip() if price_tag else "Consultar"
                    
                    resultados_normalizados.append({
                        'id': f"BENUZZI_{id_publicacion}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Benuzzi'
                    })

                except Exception as e:
                    # Si falla una tarjeta, la saltamos pero seguimos con las otras
                    print(f"Error parseando tarjeta: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Benuzzi: {e}")

        return resultados_normalizados
