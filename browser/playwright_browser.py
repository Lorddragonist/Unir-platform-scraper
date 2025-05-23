from playwright.async_api import async_playwright, Page, Browser as PlaywrightBrowser, ElementHandle
from interfaces.browser import Browser
import asyncio

class PlaywrightBrowserImpl(Browser):
    """Implementación del navegador usando Playwright"""

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
        self.errorInitialize = "Navegador no inicializado"
    
    async def initialize(self, **kwargs) -> None:
        """Inicializa el navegador"""
        headless = kwargs.get("headless", False)
        viewport = kwargs.get("viewport", {"width": 1920, "height": 1080})
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page(viewport=viewport)
        
    async def navigate(self, url: str) -> None:
        """Navega a la URL especificada"""
        if not self.page:
            raise RuntimeError(self.errorInitialize)
        await self.page.goto(url)
        await self.page.wait_for_load_state('networkidle')
        
    async def get_current_url(self) -> str:
        """Obtiene la URL actual de la página"""
        if not self.page:
            raise RuntimeError(self.errorInitialize)
        return self.page.url
        
    async def wait_for_selector(self, selector: str, timeout: int = 5000) -> bool:
        """Espera a que el selector especificado esté presente en la página"""
        if not self.page:
            raise RuntimeError(self.errorInitialize)
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except TimeoutError:
            return False
        
    def get_element_by_selector(self, selector: str, **kwargs) -> ElementHandle:
        """Obtiene el elemento especificado por el selector"""
        if not self.page:
            raise RuntimeError(self.errorInitialize)
        return self.page.locator(selector, **kwargs)
        
    async def click(self, selector: str, **kwargs) -> None:
        """Clickea en el elemento especificado"""
        if not self.page:
            raise RuntimeError(self.errorInitialize)
        await self.page.click(selector, **kwargs)
        
    async def fill(self, selector: str, text: str) -> None:
        """Escribe el texto especificado en el elemento especificado"""
        if not self.page:
            raise RuntimeError(self.errorInitialize)
        await self.page.fill(selector, text)
        
    async def wait_for_timeout(self, timeout: int) -> None:
        """Espera el tiempo especificado"""
        if not self.page:
            raise RuntimeError(self.errorInitialize)
        await self.page.wait_for_timeout(timeout)
        
    async def close(self) -> None:
        """Cierra el navegador"""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
        
