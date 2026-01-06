import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class GuastavinoScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Guastavino ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
        
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Guastavino")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las tarjetas de los productos con la clase correcta
            cards = soup.select('article.rh_list_card')

            for card in cards:
                try:
                    # Título y Link
                    title_tag = card.select_one('.rh_list_card__details h3 a')
                    if not title_tag:
                        continue
                        
                    titulo = title_tag.text.strip()
                    link = title_tag['href']

                    # Descripción
                    description_tag = card.select_one('.rh_list_card__excerpt')
                    descripcion = description_tag.text.strip() if description_tag else ""
                    
                    # Precio
                    price_tag = card.select_one('.rh_list_card__priceLabel .price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # ID
                    # Intentamos obtenerlo del atributo data-propertyid en el botón de favoritos
                    fav_icon = card.select_one('.favorite-placeholder')
                    if fav_icon and fav_icon.has_attr('data-propertyid'):
                        id_publicacion = fav_icon['data-propertyid']
                    else:
                        # Fallback: intentar sacarlo de la URL o usar hash
                        id_publicacion = link.strip('/').split('/')[-1]
                    
                    resultados_normalizados.append({
                        'id': f"GUASTAVINO_{id_publicacion}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Guastavino'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Guastavino: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Guastavino: {e}")

        return resultados_normalizados
