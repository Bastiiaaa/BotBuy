import requests
import time
from datetime import datetime

# COLORES
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

# API HABBO
HABBO_API = "https://habboapi.site/api/market/history"
POLL_INTERVAL = 5  # segundos entre cada consulta
MAX_FAILED_ATTEMPTS = 5  # intentos fallidos antes de detenerse

VALID_HOTELS = ["es", "com", "de", "it", "fr", "nl", "br", "tr", "fi", "s2"]

# Índices de cada campo en los arrays del historial devueltos por la API:
# [avg_price, sold_count, credit_sum, open_offers, timestamp]
IDX_AVG_PRICE = 0
IDX_SOLD_COUNT = 1
IDX_CREDIT_SUM = 2
IDX_OPEN_OFFERS = 3
IDX_TIMESTAMP = 4


class MarketplaceBot:
    def __init__(self):
        self.furni_classname = None
        self.max_price = None
        self.hotel = "es"
        self.running = False
        self.compras_realizadas = 0

    def banner(self):
        print(f"\n{BOLD}{BLUE}")
        print("╔════════════════════════════════════╗")
        print("║   MARKETPLACE BOT v2.0 (API) ✅    ║")
        print("║   Powered by HabboAPI Official     ║")
        print("╚════════════════════════════════════╝")
        print(f"{RESET}\n")

    def obtener_parametros(self):
        """Solicita al usuario los parámetros necesarios antes de iniciar."""
        print(f"{BOLD}[BOT]{RESET} Escribe el nombre del furni a buscar:")
        self.furni_classname = input("> ").strip().lower()

        if not self.furni_classname:
            print(f"{RED}[ERROR] Debes escribir un nombre de furni{RESET}")
            return False

        print(f"\n{BOLD}[BOT]{RESET} Precio máximo a pagar (en credits):")
        try:
            self.max_price = int(input("> ").strip())
            if self.max_price <= 0:
                print(f"{RED}[ERROR] El precio debe ser un número positivo{RESET}")
                return False
        except ValueError:
            print(f"{RED}[ERROR] Debes escribir un número válido{RESET}")
            return False

        print(f"\n{BOLD}[BOT]{RESET} Hotel ({'/'.join(VALID_HOTELS)}) [default: es]:")
        hotel_input = input("> ").strip().lower()
        if hotel_input in VALID_HOTELS:
            self.hotel = hotel_input
        else:
            if hotel_input:
                print(f"{YELLOW}[BOT] Hotel no reconocido, usando hotel por defecto: es{RESET}")
            self.hotel = "es"

        return True

    def obtener_datos_mercado(self):
        """Consulta la API de HabboAPI y retorna los datos del mercadillo."""
        try:
            params = {
                "classname": self.furni_classname,
                "hotel": self.hotel,
            }

            response = requests.get(HABBO_API, params=params, timeout=10)

            if response.status_code != 200:
                print(
                    f"{RED}[ERROR] La API respondió con código {response.status_code}{RESET}"
                )
                return None

            data = response.json()

            if not data or len(data) == 0:
                print(
                    f"{RED}[ERROR] Furni '{self.furni_classname}' no encontrado en hotel '{self.hotel}'{RESET}"
                )
                return None

            furni_data = data[0]
            market_data = furni_data.get("marketData", {})
            history = market_data.get("history", [])

            if not history:
                print(
                    f"{RED}[ERROR] Sin datos de historial para '{self.furni_classname}'{RESET}"
                )
                return None

            # La última entrada del historial contiene los datos más recientes
            ultimo_dato = history[-1]

            return {
                "classname": furni_data.get("ClassName", self.furni_classname),
                "name": furni_data.get("FurniName", self.furni_classname),
                "current_price": ultimo_dato[IDX_AVG_PRICE],
                "sold_count": ultimo_dato[IDX_SOLD_COUNT],
                "credit_sum": ultimo_dato[IDX_CREDIT_SUM],
                "open_offers": ultimo_dato[IDX_OPEN_OFFERS],
                "timestamp": ultimo_dato[IDX_TIMESTAMP],
                "avg_price": market_data.get("averagePrice"),
            }

        except requests.exceptions.Timeout:
            print(f"{RED}[ERROR] Timeout – la API no respondió a tiempo{RESET}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"{RED}[ERROR] Sin conexión – comprueba tu red{RESET}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"{RED}[ERROR] Error de conexión: {e}{RESET}")
            return None
        except (KeyError, IndexError, TypeError, ValueError) as e:
            print(f"{RED}[ERROR] Error al parsear la respuesta de la API: {e}{RESET}")
            return None

    def mostrar_datos(self, datos):
        """Muestra los datos actuales del mercadillo en consola."""
        precio = datos["current_price"]
        promedio = datos["avg_price"]
        ofertas = datos["open_offers"]
        timestamp = datos["timestamp"]

        if isinstance(timestamp, str):
            tiempo_mostrar = timestamp
        else:
            tiempo_mostrar = str(timestamp)

        print(f"\n{BOLD}[BOT]{RESET} 📊 {BOLD}{datos['name']}{RESET}")
        print(f"    💵 Precio actual:    {BOLD}{precio}{RESET} credits")
        print(f"    📈 Precio promedio:  {promedio} credits")
        print(f"    🛒 Ofertas abiertas: {ofertas}")
        print(f"    ⏰ Actualizado:      {tiempo_mostrar}")

    def evaluar_compra(self, datos):
        """Decide si el precio actual está dentro del rango aceptable."""
        precio = datos["current_price"]
        if precio <= self.max_price:
            return True, "En rango"
        diferencia = precio - self.max_price
        return False, f"Muy caro (+{diferencia} credits)"

    def comprar(self, datos):
        """Registra la compra y muestra la confirmación.

        NOTE: Esta implementación es una simulación. Para una compra real dentro del
        cliente de Habbo sería necesario integrar una extensión (p.ej. G-Earth) que
        envíe el packet de compra correspondiente una vez detectado el precio objetivo.
        """
        print(f"\n{BOLD}{GREEN}[BOT]{RESET} 💰 ¡¡COMPRANDO!!")
        print(f"    ✅ Item:   {datos['name']}")
        print(f"    ✅ Precio: {datos['current_price']} credits")
        print(f"{GREEN}[BOT] Compra realizada correctamente{RESET}\n")
        self.compras_realizadas += 1

    def iniciar(self):
        """Punto de entrada principal del bot."""
        self.banner()

        if not self.obtener_parametros():
            return

        self.running = True
        print(
            f"\n{BOLD}{BLUE}[BOT]{RESET} 🔍 Monitoreando '{BOLD}{self.furni_classname}{RESET}'"
            f" en hotel '{BOLD}{self.hotel}{RESET}'"
        )
        print(f"{BLUE}[BOT]{RESET} Precio máximo: {BOLD}{self.max_price} credits{RESET}")
        print(f"{BLUE}[BOT]{RESET} ⏱️  Actualizando cada {POLL_INTERVAL} segundos...\n")

        intentos_fallidos = 0

        while self.running:
            try:
                datos = self.obtener_datos_mercado()

                if datos is None:
                    intentos_fallidos += 1
                    if intentos_fallidos >= MAX_FAILED_ATTEMPTS:
                        print(
                            f"{RED}[BOT] Demasiados errores consecutivos, deteniendo...{RESET}"
                        )
                        break
                    print(
                        f"{YELLOW}[BOT] Reintentando en {POLL_INTERVAL} segundos "
                        f"({intentos_fallidos}/{MAX_FAILED_ATTEMPTS})...{RESET}"
                    )
                    time.sleep(POLL_INTERVAL)
                    continue

                intentos_fallidos = 0
                self.mostrar_datos(datos)

                debe_comprar, razon = self.evaluar_compra(datos)

                if debe_comprar:
                    self.comprar(datos)
                    break
                else:
                    print(f"    {YELLOW}❌ {razon}{RESET}")

                time.sleep(POLL_INTERVAL)

            except KeyboardInterrupt:
                print(f"\n{YELLOW}[BOT] Bot detenido por el usuario{RESET}")
                self.running = False
                break
            except Exception as e:
                print(f"{RED}[ERROR] Error inesperado: {e}{RESET}")
                time.sleep(POLL_INTERVAL)

        print(f"\n{BOLD}{BLUE}[BOT]{RESET} ¡Hasta luego! 👋")
        print(f"    Compras realizadas: {BOLD}{self.compras_realizadas}{RESET}\n")


def main():
    bot = MarketplaceBot()
    bot.iniciar()


if __name__ == "__main__":
    main()
