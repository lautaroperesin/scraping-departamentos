from .base_scraper import BaseScraper
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import unicodedata

class SamarScraper(BaseScraper):
    def scrapear(self):
        print(f"Buscando en Samar ({self.url_base})...")
        resultados_normalizados = []
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            }
            
            response = requests.get(self.url_base, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"Error {response.status_code} al conectar con Samar")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            cards = soup.select('.property-wrap')
            
            for card in cards:
                try:
                    # Title
                    # Priority: 1. .property-title a, 2. img[alt]
                    titulo = "Sin Título"
                    title_tag = card.select_one('.property-title a')
                    if title_tag:
                        titulo = title_tag.text.strip()
                    else:
                        img = card.find('img', alt=True)
                        if img:
                            titulo = img['alt'].strip()

                    # Filter for "Departamento" if explicitly requested or implied
                    # The URL is generic /alquileres/, so we should check if it looks like a Depto
                    # Common keywords: "Departamento", "Dpto", "Piso", "Ambientes"
                    # But user asked for "Samar" generally, and main.py doesn't strictly filter yet?
                    # Actually, main.py usually sets specific URLs. URL_SAMAR is /alquileres/
                    # We can do a soft filter or just grab everything. The task doesn't specify strictly.
                    # However, to be safe, we extract type from meta if possible.
                    
                    is_depto = False
                    if "departamento" in titulo.lower() or "dpto" in titulo.lower() or "piso" in titulo.lower():
                        is_depto = True
                    
                    # Also check meta tags
                    meta_tags = card.select('.property-meta li')
                    for m in meta_tags:
                        txt = m.get_text(strip=True).lower()
                        if "dormitor" in txt or "baños" in txt:
                             # Likely a residential unit
                             pass

                    # Price
                    price_tag = card.select_one('.property-price')
                    precio = price_tag.text.strip() if price_tag else "Consultar"
                    precio = " ".join(precio.split())
                    
                    if not precio or precio == "$":
                         # Sometimes empty price means sold/rented or just placeholder
                         continue

                    # Link & ID
                    # Since <a> tags are missing/hidden, we construct the link from title.
                    # Valid pattern seems to be: https://samarpropiedades.com.ar/inmueble/{slug}/
                    # We will slugify the title.
                    
                    slug = self.slugify(titulo)
                    link = f"https://www.samarpropiedades.com.ar/inmueble/{slug}/"
                    
                    # ID
                    # We use the slug as ID since we don't have the numeric ID easily
                    id_samar = slug
                    
                    # Description / Address
                    addr_tag = card.select_one('.property-address')
                    descripcion = addr_tag.text.strip() if addr_tag else titulo

                    resultados_normalizados.append({
                        'id': f"SAMAR_{id_samar}",
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'precio': precio,
                        'link': link,
                        'portal': 'Samar'
                    })

                except Exception as e:
                    print(f"Error parseando tarjeta Samar: {e}")
                    continue

        except Exception as e:
            print(f"Error scrapeando Samar: {e}")

        return resultados_normalizados

    def slugify(self, text):
        """
        Slugify a string:
        - Normalize unicode (remove accents)
        - Lowercase
        - Replace non-alphanumeric with hyphens
        - Strip leading/trailing hyphens
        """
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '-', text)
        return text.strip('-')
