import asyncio
from browser.playwright_browser import PlaywrightBrowserImpl
from config.settings import Settings
from services.loging_service import LogingService
from services.programs_service import ProgramsService
from services.courses_service import CoursesService


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
        
        # Iniciar sesión
        login_service = LogingService(browser)
        
        await login_service.login(Settings.MOODLE_URL, Settings.MOODLE_USERNAME, Settings.MOODLE_PASSWORD)
        print("Inicio de sesión exitoso")
        
        # Obtener los programas
        programs_service = ProgramsService(browser)
        programas =await programs_service.get_programs(Settings.MOODLE_URL)
        
        # Obtener los cursos
        courses_service = CoursesService(browser)
        await courses_service.get_courses(Settings.MOODLE_URL, programas)
        
        input("Presione Enter para cerrar el navegador...")
        
        # Cerrar el navegador
        await browser.close()
        
    except Exception as e:
        print(f"Error en programa principal: {e}")

if __name__ == "__main__":
    asyncio.run(main())

