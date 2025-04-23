from abc import ABC, abstractmethod
from playwright.async_api import ElementHandle


class Browser(ABC):
    """Interfaz para el comportamiento de un navegador"""

    @abstractmethod
    async def initialize(self, **kwargs) -> None:
        """Inicializa el navegador"""
        pass
    
    @abstractmethod
    async def navigate(self, url: str) -> None:
        """Navega a la URL especificada"""
        pass
    
    @abstractmethod
    async def wait_for_selector(self, selector: str, timeout: int = 5000) -> bool:
        """Espera a que el selector especificado esté presente en la página"""
        pass
    
    @abstractmethod
    def get_element_by_selector(self, selector: str, **kwargs) -> ElementHandle:
        """Obtiene el elemento especificado por el selector"""
        pass
    
    @abstractmethod
    async def click(self, selector: str, **kwargs) -> None:
        """Clickea en el elemento especificado"""
        pass
    
    @abstractmethod
    async def fill(self, selector: str, text: str) -> None:
        """Escribe el texto especificado en el elemento especificado"""
        pass
    
    @abstractmethod
    async def wait_for_timeout(self, timeout: int) -> None:
        """Espera el tiempo especificado"""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Cierra el navegador"""
        pass
