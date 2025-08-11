"""
FastAPI middleware for automatic language detection and translation
"""

import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar

from . import detect_language_from_header, t

logger = logging.getLogger(__name__)

# Context variable to store current request language
current_language: ContextVar[str] = ContextVar('current_language', default='en')

class TranslationMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically detects user language and sets it in context
    """
    
    def __init__(self, app, default_language: str = "en"):
        super().__init__(app)
        self.default_language = default_language
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and detect language
        """
        # Detect language from Accept-Language header
        accept_language = request.headers.get("accept-language", "")
        detected_language = detect_language_from_header(accept_language)
        
        # Check for language override in query parameters or headers
        lang_override = (
            request.query_params.get("lang") or 
            request.headers.get("x-language") or
            detected_language
        )
        
        # Validate language and set in context
        if lang_override in ["en", "sv"]:  # Add more languages as needed
            current_language.set(lang_override)
        else:
            current_language.set(self.default_language)
        
        logger.debug(f"Request language set to: {current_language.get()}")
        
        # Process request
        response = await call_next(request)
        
        # Add language header to response
        if hasattr(response, 'headers'):
            response.headers["Content-Language"] = current_language.get()
        
        return response

def get_current_language() -> str:
    """Get the current request language from context"""
    return current_language.get()

def translate_for_request(key: str, **kwargs) -> str:
    """
    Translate a key using the current request language
    
    Args:
        key: Translation key
        **kwargs: Variables for string formatting
        
    Returns:
        Translated string
    """
    return t(key, get_current_language(), **kwargs)

# Convenience alias
tr = translate_for_request

class TranslatedHTTPException(Exception):
    """
    HTTP Exception that automatically translates error messages
    """
    
    def __init__(
        self, 
        status_code: int, 
        translation_key: str, 
        detail: str = None,
        headers: dict = None,
        **translation_kwargs
    ):
        self.status_code = status_code
        self.translation_key = translation_key
        self.detail = detail
        self.headers = headers
        self.translation_kwargs = translation_kwargs
    
    def get_translated_detail(self) -> str:
        """Get the translated error message"""
        if self.detail:
            return self.detail
        return translate_for_request(self.translation_key, **self.translation_kwargs)
    
    def to_response(self) -> JSONResponse:
        """Convert to FastAPI JSONResponse"""
        return JSONResponse(
            status_code=self.status_code,
            content={"detail": self.get_translated_detail()},
            headers=self.headers
        )

# Common translated exceptions
class TranslatedValidationError(TranslatedHTTPException):
    def __init__(self, field: str = None, **kwargs):
        super().__init__(
            status_code=422,
            translation_key="validation.required_field" if field else "api.validation_error",
            field=field,
            **kwargs
        )

class TranslatedNotFoundError(TranslatedHTTPException):
    def __init__(self, resource: str = "resource", **kwargs):
        super().__init__(
            status_code=404,
            translation_key="api.flow_not_found",  # Customize based on resource
            **kwargs
        )

class TranslatedUnauthorizedError(TranslatedHTTPException):
    def __init__(self, **kwargs):
        super().__init__(
            status_code=401,
            translation_key="auth.login_required",
            **kwargs
        )

class TranslatedForbiddenError(TranslatedHTTPException):
    def __init__(self, **kwargs):
        super().__init__(
            status_code=403,
            translation_key="auth.access_denied",
            **kwargs
        )

class TranslatedInternalServerError(TranslatedHTTPException):
    def __init__(self, **kwargs):
        super().__init__(
            status_code=500,
            translation_key="api.internal_error",
            **kwargs
        )

# Exception handler for FastAPI
async def translated_exception_handler(request: Request, exc: TranslatedHTTPException):
    """
    Exception handler for TranslatedHTTPException
    """
    return exc.to_response()

# Utility functions for common API responses
def success_response(translation_key: str, data: dict = None, **kwargs) -> dict:
    """
    Create a success response with translated message
    """
    response = {
        "success": True,
        "message": translate_for_request(translation_key, **kwargs)
    }
    if data:
        response["data"] = data
    return response

def error_response(translation_key: str, **kwargs) -> dict:
    """
    Create an error response with translated message
    """
    return {
        "success": False,
        "error": translate_for_request(translation_key, **kwargs)
    }
