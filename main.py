from src.scrapers.orcu import OrcuScraper
from src.scrapers.salas import SalasScraper
from src.scrapers.benuzzi import BenuzziScraper
from src.scrapers.remax import RemaxScraper
from src.scrapers.guastavino import GuastavinoScraper
from src.scrapers.bottai import BottaiScraper
from src.scrapers.taverna import TavernaScraper
from src.scrapers.menzella import MenzellaScraper
from src.scrapers.migone import MigoneScraper
from src.scrapers.argenprop import ArgenpropScraper
from src.scrapers.christen import ChristenScraper
from src.scrapers.esquivel import EsquivelScraper
from src.scrapers.samar import SamarScraper
from src.scrapers.gimenez import GimenezScraper
from src.scrapers.sauce import SauceScraper
from src.scrapers.penalva import PenalvaScraper
from src.scrapers.royo import RoyoScraper
from src.scrapers.alicandro import AlicandroScraper
from src.scrapers.raffin import RaffinScraper
from src.scrapers.weidmann import WeidmannScraper
from src.scrapers.adminymandatos import AdminymandatosScraper
from src.scrapers.lenarduzzi import LenarduzziScraper
from src.scrapers.uretacortes import UretacortesScraper
from src.scrapers.apl import AplScraper
from src.scrapers.sarricchio import SarricchioScraper
from src.scrapers.santafe_propiedades import SantaFePropiedadesScraper
from src.scrapers.concepto import ConceptoScraper
from src.scrapers.cofasa import CofasaScraper
from src.gestor_datos import GestorDatos
from src.notificador import Notificador

# URLs
URL_ORCU = "https://www.orcuinmobiliaria.com.ar/resultados"
URL_SALAS = "https://www.salasinmobiliaria.com.ar/listado.php?id_operacion=3&id_zona=36&id_tipo=5&dormitorios=2&codigo=&rango=0%3B770000"
URL_BENUZZI = "https://benuzzi.com/search-properties/?status%5B%5D=alquiler&type%5B%5D=departamento&bedrooms=2"
URL_REMAX = "https://www.remax.com.ar/listings/rent?page=0&pageSize=24&sort=-createdAt&in:operationId=2&eq:entrepreneurship=false&in:typeId=1,2,3,4,5,6,7,8&pricein=2:0:750000&eq:bedrooms=2&locations=in:::458@%3Cb%3ESanta%3C%2Fb%3E%20%3Cb%3EFe%3C%2Fb%3E%20Capital::::&landingPath=&filterCount=4&viewMode=listViewMode"
URL_GUASTAVINO = "https://guastavinoeimbert.com.ar/properties-search/?location%5B%5D=santa-fe&type%5B%5D=departamentos&status=alquiler&bedrooms=2"
URL_BOTTAI = "https://www.bottai.com.ar/inmuebles_list_Alquiler_Departamentos_2-dormitorios_seleccione_0_0"
URL_TAVERNA = "https://tavernainmobiliaria.com.ar/search-results/?status%5B%5D=alquiler&type%5B%5D=departamento&bedrooms=2&country%5B%5D=con-cochera"
URL_MENZELLA = "https://www.menzellainmobiliaria.com.ar/?u=208&pag=propiedades&op=2&idtipo2=777&idciudad=2013&idbarrio=0&dorm=0&banios=0&moneda=1&desde=&hasta=&searcher_code="
URL_MIGONE = "https://www.migoneinmobiliaria.com.ar/propiedades?p=0&b=All&ope=A&tipo=D&a1=2&cod="
URL_ARGENPROP = "https://www.argenprop.com/departamentos/alquiler/santa-fe-la-capital/2-dormitorios/pesos-hasta-750000?&solo-ver-pesos"
URL_CHRISTEN = "https://www.christen.com.ar/Buscar?operation=2&ptypes=2&tags=3&suites=2&o=2,2&1=1"
URL_SAUCE = "https://www.sauce.com.ar/properties/?filter-contract=RENT&filter-property-type=24&filter-location=&filter-rooms=2"
URL_URBANO = "https://urbano-inmobiliaria.com/web/alquileres.php"
URL_GIMENEZ = "https://www.gimenezinmobiliaria.com.ar/listing?state=21&city=12432&purpose=rent&type=Departamento&beds=2&q=&user_id=508&shortBy=null&min_price=&max_price="
URL_ESQUIVEL = "https://www.esquivelinmobiliaria.com.ar/resultados.php?bus=av&op=A&tipo=1&zona=&dor=2"
URL_SAMAR = "https://www.samarpropiedades.com.ar/alquileres/"
URL_PENALVA = "https://penalvainmobiliaria.com.ar/resultados/?property-id&location=santa-fe&status=alquiler&type=departamentos&bedrooms=2"
URL_ROYO = "https://www.royoinmobiliaria.com.ar/Buscar?operation=2&ptypes=2&suites=2&o=2,2&1=1"
URL_LENARDUZZI = "https://lenarduzzi.com.ar/half-map/?location=santa-fe&type=departamento&status=alquiler&bedrooms=2"
URL_RAFFIN = "https://www.raffininmobiliaria.com.ar/listing?state=21&city=12432&purpose=rent&type=&beds=2&q=&user_id=1137&shortBy=null&min_price=&max_price="
URL_APL = "https://www.aplinmobiliaria.com/propiedades?operacion=58f554bf615347788ff291d2&franquicia=&ciudad%5B%5D=58bac0b35a9f803452303225&tipo_propiedad%5B%5D=58f5563d988e744fda7edae3&dormitorios=2&moneda=%24&min=&max="
URL_CONCEPTO = "https://www.conceptonegociosinmobiliarios.com.ar/Buscar-Departamento-en-Alquiler?suites=2"
URL_SARRICCHIO = "https://sarricchio.com/index.php?operation_type=2&id_tipo_propiedad=1&numero_ambientes_propiedad=2&id_localidad=&Itemid=101&option=com_siiweb&view=properties&mod_inteliarsii_search=1"
URL_WEIDMANN = "https://inmobiliariaweidmann.com.ar/listing?state=21&city=12432&purpose=rent&type=Departamento&beds=2&q=&user_id=416&shortBy=null&min_price=&max_price="
URL_ALICANDRO = "https://www.alicandro.com.ar/Buscar?operation=2&ptypes=2&suites=2&o=2,2&1=1"
URL_URETACORTES = "https://uretacortes.com.ar/?s=&tipo=departamento&operacion=alquiler&location=santa-fe&moneda=pesos&price_low=&price_high="
URL_SANTAFE_PROPIEDADES = "https://www.santafe-propiedades.com.ar/resultados.php?descripcion=&tipoPropiedad=2&barrio=0&tipo=A"
URL_ADMINYMANDATOS = "https://administracionesymandatos.com.ar/listing?state=21&city=12432&purpose=rent&type=Departamento&beds=2&q=&user_id=1566&shortBy=null&min_price=&max_price="
URL_COFASA = "https://www.cofasainmobiliaria.com.ar/Buscar-Departamento-en-Alquiler-en-Santa-Fe-45679?suites=2"


def main():
    print("Iniciando búsqueda...")
    
    # 1. Instanciamos el gestor (cargará el JSON automáticamente) y el notificador
    gestor = GestorDatos()
    notificador = Notificador()
    
    scrapers = [
        OrcuScraper(URL_ORCU),
        SalasScraper(URL_SALAS),
        BenuzziScraper(URL_BENUZZI),
        RemaxScraper(URL_REMAX),
        GuastavinoScraper(URL_GUASTAVINO),
        BottaiScraper(URL_BOTTAI),
        TavernaScraper(URL_TAVERNA),
        MenzellaScraper(URL_MENZELLA),
        MigoneScraper(URL_MIGONE),
        ArgenpropScraper(URL_ARGENPROP),
        ChristenScraper(URL_CHRISTEN),
        EsquivelScraper(URL_ESQUIVEL),
        SamarScraper(URL_SAMAR),
        GimenezScraper(URL_GIMENEZ),
        SauceScraper(URL_SAUCE),
        PenalvaScraper(URL_PENALVA),
        RoyoScraper(URL_ROYO),
        LenarduzziScraper(URL_LENARDUZZI),
        RaffinScraper(URL_RAFFIN),
        AplScraper(URL_APL),
        ConceptoScraper(URL_CONCEPTO),
        SarricchioScraper(URL_SARRICCHIO),
        WeidmannScraper(URL_WEIDMANN),
        AlicandroScraper(URL_ALICANDRO),
        UretacortesScraper(URL_URETACORTES),
        SantaFePropiedadesScraper(URL_SANTAFE_PROPIEDADES),
        AdminymandatosScraper(URL_ADMINYMANDATOS),
        CofasaScraper(URL_COFASA)
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