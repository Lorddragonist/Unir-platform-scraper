import asyncio
from browser.playwright_browser import PlaywrightBrowserImpl
from config.settings import Settings


async def main():
    try:
        # Validar las variables de entorno
        try:
            Settings.validate()
        except ValueError as e:
            print(f"Error en variables de entorno: {e}")
            return
        
        # Inicializar el navegador
        browser = PlaywrightBrowserImpl()
        await browser.initialize(
            headless=Settings.HEADLESS,
            viewport_width=Settings.VIEWPORT_WIDTH,
            viewport_height=Settings.VIEWPORT_HEIGHT
        )
        
        # Navegar a la página de inicio de sesión de Moodle
        await browser.navigate(Settings.MOODLE_URL)
        
        input("Presione Enter para cerrar el navegador...")
        
        # Cerrar el navegador
        await browser.close()
        
    except Exception as e:
        print(f"Error en programa principal: {e}")

if __name__ == "__main__":
    asyncio.run(main())

