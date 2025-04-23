import asyncio
from interfaces.browser import Browser


class CoursesService:
    """Servicio para obtener los cursos de cada programa"""

    def __init__(self, browser: Browser):
        self.browser = browser

    async def get_courses(self, url: str) -> list[dict]:
        """Obtiene los cursos de los programas"""
        courses_list = []

        try:
            # Navegar a la URL de la plataforma Moodle si no se ha navegado aún
            current_url = await self.browser.get_current_url()
            if current_url != url:
                await self.browser.navigate(url)
                await self.browser.wait_for_timeout(1000)

            # Obtener elemento navbar lateral de Moodle que contiene los programas
            navbar_lateral = self.browser.get_element_by_selector(".list-group").nth(0)
            if navbar_lateral:
                # Obtener cursos de la navbar lateral
                cursos = navbar_lateral.locator("a.list-group-item.coursenode")

                # Obtener numero de cursos
                numero_cursos = await cursos.count()
                print(f"Numero de cursos: {numero_cursos}")

                # Obtener nombre de cada programa
                for i in range(numero_cursos):
                    nombre_cursos = (
                        await cursos.nth(i).locator("span").nth(1).text_content()
                    )
                    link_curso = await cursos.nth(i).get_attribute("href")

                    courses_list.append(
                        {
                            "nombre": nombre_cursos,
                            "link": link_curso,
                        }
                    )

                return courses_list

        except Exception as e:
            print(f"Error al obtener los cursos: {e}")
            return []
