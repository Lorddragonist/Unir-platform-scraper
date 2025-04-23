import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuración de la aplicación"""

    MOODLE_URL = os.getenv("MOODLE_URL")
    MOODLE_USERNAME = os.getenv("MOODLE_USERNAME")
    MOODLE_PASSWORD = os.getenv("MOODLE_PASSWORD")
    
    # Configuración del navegador
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
    print(f"HEADLESS: {HEADLESS}")
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", 1920))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", 1080))
    
    @classmethod
    def validate(cls) -> None:
        """Valida que las variables de entorno estén correctamente configuradas"""
        required = ["MOODLE_URL", "MOODLE_USERNAME", "MOODLE_PASSWORD"]
        missing = [field for field in required if not getattr(cls, field)]
        
        if missing:
            raise ValueError(f"Variables de entorno faltantes: {', '.join(missing)}")
    
        
