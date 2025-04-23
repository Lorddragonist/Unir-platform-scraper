import asyncio
from interfaces.browser import Browser

class CoursesService:
    """Servicio para obtener los cursos de cada programa"""

    def __init__(self, browser: Browser):
        self.browser = browser
        
    async def get_courses(self, url: str, programs: list[dict]) -> None:
        """Obtiene los cursos de un programa"""
        
        try:
                
            
            # Ir a la url
            await self.browser.navigate(url)
            await self.browser.wait_for_timeout(1000)
            
            # Obtener los cursos de cada programa
            for program in programs:
                # identificar el programa en la pagina
                program_element = self.browser.get_element_by_selector("span.media-body", has_text=f"{program['nombre']}")
                                
                cursos = []
                # Obtener los cursos del programa
                cursos_element = program_element.locator("a.list-group-item.coursenode")
                numero_cursos = await cursos_element.count()
                print(f"Numero de cursos: {numero_cursos}")
                
                # Obtener los cursos del programa
                for i in range(numero_cursos):
                    curso_element = cursos_element.nth(i)
                    curso_nombre = await curso_element.locator("span").nth(1).text_content()
                    cursos.append(curso_nombre)
                    
                print(f"Cursos del programa {program['nombre']}: {cursos}")
                
        except Exception as e:
            print(f"Error al obtener los cursos: {e}")
            
