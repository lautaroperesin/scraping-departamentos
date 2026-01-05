from src.scrapers.orcu import OrcuScraper
from src.scrapers.salas import SalasScraper
from src.gestor_datos import GestorDatos
from src.notificador import Notificador

# URLs
URL_ORCU = "https://www.orcuinmobiliaria.com.ar/resultados"
URL_SALAS = "https://www.salasinmobiliaria.com.ar/listado.php?id_operacion=3&id_zona=36&id_tipo=5&dormitorios=2&codigo=&rango=0%3B770000"

def main():
    print("Iniciando búsqueda...")
    
    # 1. Instanciamos el gestor (cargará el JSON automáticamente) y el notificador
    gestor = GestorDatos()
    notificador = Notificador()
    
    scrapers = [
        OrcuScraper(URL_ORCU),
        SalasScraper(URL_SALAS),
    ]

    nuevos_hallazgos = []

    # 2. Scrapeamos y filtramos en el momento
    for scraper in scrapers:
        propiedades = scraper.scrapear()
        
        for prop in propiedades:
            if gestor.es_nuevo(prop['id']):
                nuevos_hallazgos.append(prop)
                gestor.registrar_id(prop['id'])

    # 3. Procesamos los resultados nuevos
    if nuevos_hallazgos:
        print(f"¡Encontrados {len(nuevos_hallazgos)} departamentos nuevos!")
        # notificador.enviar_mensaje(f"¡Encontrados {len(nuevos_hallazgos)} departamentos nuevos!")
        
        for depto in nuevos_hallazgos:
            # Enviar a Telegram
            notificador.formatear_y_enviar(depto)
            print(f" > Notificación enviada: {depto['titulo']}")
        
        # 4. Guardamos los cambios en el archivo JSON
        gestor.guardar_cambios()
        print("Base de datos actualizada.")
    else:
        print("No se encontraron propiedades nuevas.")

if __name__ == "__main__":
    main()