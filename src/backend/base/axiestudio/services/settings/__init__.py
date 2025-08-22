from . import factory, service
from .base import Settings

# Create a global settings instance
settings = Settings()

__all__ = ["factory", "service", "settings", "Settings"]
