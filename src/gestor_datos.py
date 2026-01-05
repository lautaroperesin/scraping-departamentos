import json
import os

class GestorDatos:
    def __init__(self, archivo='departamentos.json'):
        self.archivo = archivo
        self.ids_vistos = self._cargar_datos()

    def _cargar_datos(self) -> set:
        """Carga los IDs del archivo JSON si existe."""
        if not os.path.exists(self.archivo):
            return set()
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                lista_ids = json.load(f)
                return set(lista_ids)
        except (json.JSONDecodeError, IOError):
            # Si el archivo está corrupto o vacío, arrancamos de cero
            return set()

    def es_nuevo(self, id_propiedad: str) -> bool:
        """Devuelve True si el ID no está en la base de datos."""
        return id_propiedad not in self.ids_vistos

    def registrar_id(self, id_propiedad: str):
        """Agrega un ID a la memoria (sin guardar a disco todavía)."""
        self.ids_vistos.add(id_propiedad)

    def guardar_cambios(self):
        """Persiste los datos en memoria al archivo JSON."""
        with open(self.archivo, 'w', encoding='utf-8') as f:
            # JSON no soporta sets, hay que convertir a lista
            json.dump(list(self.ids_vistos), f, indent=4)