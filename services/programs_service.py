import asyncio
from interfaces.browser import Browser

class ProgramsService:
    """Servicio para obtener los programas de la plataforma Moodle"""

    def __init__(self, browser: Browser):
        self.browser = browser

    async def get_programs(self, url: str) -> list[dict]:
        """Obtiene los programas de la plataforma Moodle"""
        
        programas_list = []
        
        try:
            await self.browser.navigate(url)
            await self.browser.wait_for_timeout(1000)
            
            # Obtener elemento navbar lateral de Moodle que contiene los programas
            navbar_lateral = self.browser.get_element_by_selector(".list-group").nth(0)
            if navbar_lateral:
                # Obtener programas de la navbar lateral
                programas = navbar_lateral.locator("a.list-group-item.categorynode")
                
                # Obtener numero de programas
                numero_programas = await programas.count()
                print(f"Numero de programas: {numero_programas}")
                
                # Obtener nombre de cada programa
                for i in range(numero_programas):
                    nombre_programa = await programas.nth(i).locator("span").nth(1).text_content()
                    programas_list.append({'nombre': nombre_programa})
                    print(f"Programa {i+1}: {nombre_programa}")
                
                return programas_list
                        
        except Exception as e:
            print(f'Error al obtener los programas: {e}')
            return []
            

