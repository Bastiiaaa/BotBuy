# BotBuy – Marketplace Bot v2.0

Bot automático para monitorear y comprar furnis en el mercadillo de Habbo Hotel.
Utiliza la API oficial de HabboAPI (`habboapi.site`) para obtener datos en tiempo real.

## Requisitos

- Python 3.8+
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python marketplace_bot.py
```

El bot te pedirá tres datos antes de comenzar:

1. **Nombre del furni** (classname) que deseas buscar
2. **Precio máximo** en credits que estás dispuesto a pagar
3. **Hotel** (`es`, `com`, `de`, `it`, `fr`, `nl`, `br`, `tr`, `fi`, `s2`) – por defecto `es`

### Ejemplo de sesión

```
╔════════════════════════════════════╗
║   MARKETPLACE BOT v2.0 (API) ✅    ║
║   Powered by HabboAPI Official     ║
╚════════════════════════════════════╝

[BOT] Escribe el nombre del furni a buscar:
> costurero

[BOT] Precio máximo a pagar (en credits):
> 5

[BOT] Hotel (es/com/de/it/fr/nl/br/tr/fi/s2) [default: es]:
> es

[BOT] 🔍 Monitoreando 'costurero' en hotel 'es'
[BOT] Precio máximo: 5 credits
[BOT] ⏱️  Actualizando cada 5 segundos...

[BOT] 📊 Costurero
    💵 Precio actual:    7 credits
    📈 Precio promedio:  4 credits
    🛒 Ofertas abiertas: 6
    ⏰ Actualizado:      2026-03-26 18:32:26
    ❌ Muy caro (+2 credits)

[BOT] 📊 Costurero
    💵 Precio actual:    5 credits
    📈 Precio promedio:  4 credits
    🛒 Ofertas abiertas: 2
    ⏰ Actualizado:      2026-03-26 18:32:31
    💰 ¡¡COMPRANDO!!
```

## Características

- ✅ Sin parsing de packets binarios
- ✅ Datos JSON limpios desde la API oficial
- ✅ Monitoreo continuo cada 5 segundos
- ✅ Reintentos automáticos ante errores de red
- ✅ Interfaz en consola con colores
- ✅ Fácil de mantener y depurar
