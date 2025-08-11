"""
Translation service for Axiestudio backend
Provides runtime translation support for API responses and system messages
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from functools import lru_cache

logger = logging.getLogger(__name__)

class TranslationService:
    """
    Translation service that loads and manages translations for the backend
    """
    
    def __init__(self, translations_dir: Optional[Path] = None):
        self.translations_dir = translations_dir or Path(__file__).parent
        self._translations: Dict[str, Dict[str, Any]] = {}
        self._load_translations()
    
    def _load_translations(self) -> None:
        """Load all translation files from the translations directory"""
        try:
            for locale_file in self.translations_dir.glob("*.json"):
                locale = locale_file.stem
                try:
                    with open(locale_file, 'r', encoding='utf-8') as f:
                        self._translations[locale] = json.load(f)
                    logger.info(f"Loaded translations for locale: {locale}")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse translation file {locale_file}: {e}")
                except Exception as e:
                    logger.error(f"Failed to load translation file {locale_file}: {e}")
        except Exception as e:
            logger.error(f"Failed to load translations: {e}")
    
    def reload_translations(self) -> None:
        """Reload all translation files (useful for development)"""
        self._translations.clear()
        self._load_translations()
    
    def get_available_locales(self) -> list[str]:
        """Get list of available locales"""
        return list(self._translations.keys())
    
    def translate(self, key: str, locale: str = "en", **kwargs) -> str:
        """
        Translate a key to the specified locale
        
        Args:
            key: Translation key in dot notation (e.g., 'api.flow_not_found')
            locale: Target locale (default: 'en')
            **kwargs: Variables for string formatting
            
        Returns:
            Translated string or the key if translation not found
        """
        if locale not in self._translations:
            logger.warning(f"Locale '{locale}' not available, falling back to 'en'")
            locale = "en"
        
        if locale not in self._translations:
            logger.error("No translations available, returning key")
            return key
        
        # Navigate through nested dictionary using dot notation
        translation_data = self._translations[locale]
        keys = key.split('.')
        
        try:
            for k in keys:
                translation_data = translation_data[k]
            
            # Format string with provided variables
            if kwargs:
                return translation_data.format(**kwargs)
            return translation_data
            
        except (KeyError, TypeError):
            logger.warning(f"Translation key '{key}' not found for locale '{locale}'")
            # Fallback to English if available
            if locale != "en" and "en" in self._translations:
                return self.translate(key, "en", **kwargs)
            return key
    
    def has_translation(self, key: str, locale: str = "en") -> bool:
        """Check if a translation exists for the given key and locale"""
        if locale not in self._translations:
            return False
        
        translation_data = self._translations[locale]
        keys = key.split('.')
        
        try:
            for k in keys:
                translation_data = translation_data[k]
            return True
        except (KeyError, TypeError):
            return False


# Global translation service instance
_translation_service: Optional[TranslationService] = None

def get_translation_service() -> TranslationService:
    """Get the global translation service instance"""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service

def t(key: str, locale: str = "en", **kwargs) -> str:
    """
    Convenience function for translation
    
    Args:
        key: Translation key in dot notation
        locale: Target locale
        **kwargs: Variables for string formatting
        
    Returns:
        Translated string
    """
    return get_translation_service().translate(key, locale, **kwargs)

def reload_translations() -> None:
    """Reload all translations (useful for development)"""
    global _translation_service
    if _translation_service:
        _translation_service.reload_translations()

# Language detection utilities
def detect_language_from_header(accept_language: str) -> str:
    """
    Detect preferred language from Accept-Language header
    
    Args:
        accept_language: Accept-Language header value
        
    Returns:
        Detected locale code
    """
    if not accept_language:
        return "en"
    
    # Parse Accept-Language header (simplified)
    # Format: "en-US,en;q=0.9,sv;q=0.8"
    languages = []
    for lang_part in accept_language.split(','):
        lang_part = lang_part.strip()
        if ';' in lang_part:
            lang, quality = lang_part.split(';', 1)
            try:
                q = float(quality.split('=')[1])
            except (IndexError, ValueError):
                q = 1.0
        else:
            lang, q = lang_part, 1.0
        
        # Extract primary language code
        lang_code = lang.split('-')[0].lower()
        languages.append((lang_code, q))
    
    # Sort by quality and return the best match
    languages.sort(key=lambda x: x[1], reverse=True)
    
    service = get_translation_service()
    available_locales = service.get_available_locales()
    
    for lang_code, _ in languages:
        if lang_code in available_locales:
            return lang_code
    
    return "en"  # Default fallback
