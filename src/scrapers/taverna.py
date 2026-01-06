from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup

class TavernaScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Taverna ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            # Taverna (WordPress/Houzez) suele requerir User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(self.url_base, headers=headers)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Taverna")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos las tarjetas de propiedad.
            # En el HTML analizado vimos 'item-wrap item-wrap-v6'
            cards = soup.select('.item-wrap')

            for card in cards:
                try:
                    # El selector de título cambia según la versión de la tarjeta (v3 vs v6)
                    # pero suele ser .item-title a
                    title_tag = card.select_one('.item-title a')
                    if not title_tag:
                        # Si es un widget destacado v3 a veces el título esta en otro lado o estructura
                        # Pero para resultados de busqueda v6 está ahi.
                        continue
                        
                    titulo = title_tag.text.strip()
                    link = title_tag['href']

                    # ID
                    # Intentamos sacar el data-listid de los iconos de herramientas
                    fav_icon = card.select_one('.add-favorite-js, .item-tool-favorite, .houzez_compare')
                    if fav_icon and fav_icon.has_attr('data-listid'):
                        id_taverna = fav_icon['data-listid']
                    elif fav_icon and fav_icon.has_attr('data-listing_id'):
                        id_taverna = fav_icon['data-listing_id'] # A veces es data-listing_id en compare
                    else:
                        # Fallback: slug de la URL
                        id_taverna = link.strip('/').split('/')[-1]
                    
                    # Precio
                    # En v6: ul.item-price-wrap li.item-price
                    price_tag = card.select_one('.item-price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"

                    # Descripción / Dirección
                    # En v6 no vimos descripción explicita, intentamos .item-address si existe (v3 la tiene)
                    address_tag = card.select_one('.item-address')
                    if address_tag:
                        descripcion = address_tag.text.strip()
                    else:
                        # Si no hay address, usamos el título como descripcion ya que suele ser la dirección
                        descripcion = titulo

                    resultados_normalizados.append({
                        'id': f"TAVERNA_{id_taverna}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Taverna'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Taverna: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Taverna: {e}")

        return resultados_normalizados
