import asyncio
from interfaces.browser import Browser

class LogingService:
    """Servicio para el proceso de inicio de sesión en Moodle"""

    def __init__(self, browser: Browser):
        self.browser = browser

    async def login(self, url: str, username: str, password: str) -> bool:
        """Inicia sesión en Moodle"""
        
        try:
            await self.browser.navigate(url)
            await self.browser.wait_for_timeout(1000)
        
            # Validar si se presenta el banner de cookies
            cookies_banner = await self.browser.wait_for_selector("#truste-consent-button")
            if cookies_banner:
                await self.browser.click("#truste-consent-button")
                await self.browser.wait_for_timeout(1000)
                
            # Ingresar el nombre de usuario
            username_input = await self.browser.wait_for_selector("#Username")
            if username_input:
                await self.browser.fill("#Username", username)
                await self.browser.wait_for_timeout(1000)
            
            # Ingresar la contraseña
            password_input = await self.browser.wait_for_selector("#Password")
            if password_input:
                await self.browser.fill("#Password", password)
                await self.browser.wait_for_timeout(1000)
                
            # Ingresar el botón de inicio de sesión
            login_button = await self.browser.wait_for_selector('input.button.primary[type="submit"]')
            if login_button:
                await self.browser.click('input.button.primary[type="submit"]')
                await self.browser.wait_for_timeout(1000)
                

            return True
        except Exception as e:
            print(f"Error en el proceso de inicio de sesión: {e}")
            return False

