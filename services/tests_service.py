import asyncio
import os
import pandas as pd
from interfaces.browser import Browser


class TestsService:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.calificaciones_path = os.path.join(
            os.getcwd(),
            "calificaciones"
        )

    async def get_tests(self, course: dict) -> list[dict]:
        """Obtiene los tests de un curso"""
        try:

            tests = []

            # Navegar al curso
            current_url = await self.browser.get_current_url()
            if current_url != course["link"]:
                await self.browser.navigate(course["link"])
                await self.browser.wait_for_timeout(1000)

            # Obtener elemento navbar lateral de Moodle que contiene el menu
            resultado_actividades = self.browser.get_element_by_selector(
                'span:text("Resultado de actividades")'
            )
            if resultado_actividades:
                # Obtener cursos de la navbar lateral
                print("resultado_actividades encontrado")
                await resultado_actividades.click()
                await self.browser.page.wait_for_load_state("networkidle")

                print("resultado_actividades cargado")

                test_links = self.browser.page.locator('a:has-text("Test Tema")')

                if test_links:
                    print("test_links encontrado")
                    cantidad_de_tests = await test_links.count()
                    print(f"Cantidad de tests: {cantidad_de_tests}")

                    for i in range(cantidad_de_tests):
                        test_link = await test_links.nth(i).get_attribute("href")
                        test_row = test_links.nth(i).locator("xpath=ancestor::tr")
                        grade = await test_row.locator("xpath=./td[1]").text_content()

                        tests.append(
                            {"name": f"Test {i+1}", "link": test_link, "grade": grade}
                        )
                        
                    df = pd.DataFrame(tests)
                    df.to_csv(os.path.join(self.calificaciones_path, f"calificaciones_{course['nombre']}.csv"), index=False)
                        
                    print(f"Calificaciones guardadas en {self.calificaciones_path}")

                return tests

        except Exception as e:
            print(f"Error al navegar al curso: {e}")
            return []
