from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    """Clase abstracta que define cómo debe comportarse un scraper."""

    def __init__(self, url_base):
        self.url_base = url_base

    @abstractmethod
    def scrapear(self) -> List[Dict]:
        """
        Debe devolver una lista de diccionarios con formato estandarizado:
        [
            {
                'id': 'ID_UNICO_DEL_SITIO',
                'titulo': 'Depto centro',
                'precio': 500000,
                'ubicacion': 'San Jerónimo 3000',
                'link': 'https://...',
                'portal': 'MercadoLibre'
            },
            ...
        ]
        """
        pass