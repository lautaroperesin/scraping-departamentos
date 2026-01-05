import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Notificador:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def enviar_mensaje(self, mensaje):
        """Envía un mensaje de texto simple a Telegram."""
        if not self.token or not self.chat_id:
            print("ERROR: Faltan configurar el TOKEN o CHAT_ID en el .env")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": mensaje,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code != 200:
                print(f"Error enviando a Telegram: {response.text}")
        except Exception as e:
            print(f"Excepción al enviar telegram: {e}")

    def formatear_y_enviar(self, propiedad):
        """Recibe un diccionario de propiedad y lo manda bonito."""
        
        # Armamos un mensaje con formato Markdown
        texto = (
            f"🏠 *NUEVO DEPARTAMENTO ENCONTRADO*\n\n"
            f"💰 *Precio:* {propiedad['precio']}\n"
            f"📍 *Título:* {propiedad['titulo']}\n"
            f"🗒️ *Descripción:* {propiedad['descripcion']}\n"
            f"🔗 [Ver en {propiedad['portal']}]({propiedad['link']})"
        )
        
        self.enviar_mensaje(texto)