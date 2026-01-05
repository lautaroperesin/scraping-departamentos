import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class OrcuScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Orcu ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
            
            # Datos del formulario para filtrar:
            # operacion=A (Alquiler)
            # tipos[]=2 (Departamento)
            # dormitorios[]=2 (2 dormitorios)
            # cochera=0 (Sin cochera)
            payload = {
                'operacion': 'A',
                'tipos[]': '2',
                'dormitorios[]': '2',
                'cochera': '0'
            }
            
            response = requests.post(self.url_base, headers=headers, data=payload)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Orcu")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las tarjetas de los productos (Estructura propia de Orcu)
            cards = soup.select('.card-deck .card')

            for card in cards:
                try:
                    # Saltamos spacers o tarjetas vacías si las hay
                    if 'border:none' in card.get('style', ''):
                        continue

                    title_tag = card.find('h5', class_='card-title')
                    if not title_tag:
                        continue
                        
                    titulo = title_tag.text.strip()
                    
                    link_tag = title_tag.find('a')
                    if not link_tag:
                        continue
                    link = link_tag['href']
                    
                    # El ID está en la URL: .../detalles/12345/TITULO...
                    try:
                        id_publicacion = link.split('/detalles/')[1].split('/')[0]
                    except:
                        id_publicacion = link[-10:] # Fallback

                    # En la tarjeta de Orcu no aparece el precio explícitamente en el HTML analizado
                    # Se asume "Consultar" o se tendría que entrar al detalle.
                    precio = "Consultar" # Default por ahora
                    
                    resultados_normalizados.append({
                        'id': f"ORCU_{id_publicacion}",
                        'titulo': titulo,
                        'precio': precio,
                        'link': link,
                        'portal': 'Orcu Inmobiliaria'
                    })

                except Exception as e:
                    # Si falla una tarjeta, la saltamos pero seguimos con las otras
                    print(f"Error parseando tarjeta: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Orcu: {e}")

        return resultados_normalizados
