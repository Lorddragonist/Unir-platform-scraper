import asyncio
from browser.playwright_browser import PlaywrightBrowserImpl
from config.settings import Settings
from services.loging_service import LogingService
from services.courses_service import CoursesService
from services.tests_service import TestsService


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
        
        # Obtener los cursos
        courses_service = CoursesService(browser)
        programas = await courses_service.get_courses(Settings.MOODLE_URL)
        
        print("Cursos obtenidos exitosamente")
        
        # Imprimir el nombre de cada curso con su opcion para seleccionar
        for index, curso in enumerate(programas):
            print(f"{index + 1} - {curso['nombre']}")
        
        # Obtener la opcion del usuario
        opcion = 1 # int(input("Seleccione el curso que desea descargar: "))
        
        # Mostrar el nombre del curso seleccionado
        print(f"Descargando curso: {programas[opcion - 1]['nombre']}")
        
        # Obtener los tests del curso
        curso = programas[opcion - 1]
        
        tests_service = TestsService(browser)
        tests = await tests_service.get_tests(curso)
        
        print(tests)
        
        input("Presione Enter para cerrar el navegador...")
        
        # Cerrar el navegador
        await browser.close()
        
    except Exception as e:
        print(f"Error en programa principal: {e}")

if __name__ == "__main__":
    asyncio.run(main())

