import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class GimenezScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Gimenez ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Gimenez")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las tarjetas de los productos
            cards = soup.select('.thumbnail_one')

            for card in cards:
                try:
                    # Titulo
                    title_tag = card.select_one('.thum_title h5 a')
                    if not title_tag:
                        continue
                    # Preferimos el atributo title si existe, si no el texto
                    titulo = title_tag.get('title', title_tag.text.strip())
                    
                    # Link
                    link = title_tag['href']
                    
                    # ID extraction: "Código: 139786" -> 139786
                    id_tag = card.select_one('.thum_title h7')
                    if id_tag:
                        id_text = id_tag.text.strip() # "Código: 139786"
                        # Extraemos solo el numero
                        id_publicacion = id_text.replace('Código:', '').strip()
                    else:
                        # Fallback al link si no encontramos el codigo
                        id_publicacion = link.split('/')[-1]

                    # Precio
                    # El precio esta en un p con clase sale dentro de area_price
                    price_tag = card.select_one('.area_price .sale')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # Descripcion (Ubicación)
                    description_tag = card.select_one('.thum_title p')
                    descripcion = description_tag.text.strip() if description_tag else ""
                    
                    resultados_normalizados.append({
                        'id': f"GIMENEZ_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'descripcion': descripcion,
                        'link': link,
                        'portal': 'Gimenez Inmobiliaria'
                    })

                except Exception as e:
                    # Si falla una tarjeta, la saltamos pero seguimos con las otras
                    print(f"Error parseando tarjeta Gimenez: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Gimenez: {e}")

        return resultados_normalizados
