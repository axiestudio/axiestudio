"""
Example integration of translation service into FastAPI backend
This shows how to use the translation system in your API routes
"""

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import logging

# Import our translation system
from translations import t, get_translation_service
from translations.middleware import (
    TranslationMiddleware, 
    get_current_language,
    translate_for_request,
    TranslatedHTTPException,
    TranslatedValidationError,
    TranslatedNotFoundError,
    success_response,
    error_response,
    translated_exception_handler
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Axiestudio API with i18n")

# Add translation middleware
app.add_middleware(TranslationMiddleware, default_language="en")

# Add exception handler for translated exceptions
app.add_exception_handler(TranslatedHTTPException, translated_exception_handler)

# Example: Flow management endpoints with translation

@app.get("/api/flows")
async def get_flows(request: Request):
    """Get all flows with translated messages"""
    try:
        # Simulate getting flows from database
        flows = [
            {"id": 1, "name": "Example Flow", "status": "active"},
            {"id": 2, "name": "Test Flow", "status": "inactive"}
        ]
        
        return success_response(
            "flows.retrieved_successfully",  # Translation key
            data={"flows": flows, "count": len(flows)}
        )
        
    except Exception as e:
        logger.error(f"Error retrieving flows: {e}")
        raise TranslatedHTTPException(
            status_code=500,
            translation_key="api.internal_error"
        )

@app.post("/api/flows")
async def create_flow(flow_data: Dict[str, Any], request: Request):
    """Create a new flow with translated validation"""
    
    # Validate required fields
    if not flow_data.get("name"):
        raise TranslatedValidationError(field="name")
    
    if len(flow_data["name"]) < 3:
        raise TranslatedHTTPException(
            status_code=422,
            translation_key="validation.min_length",
            min=3
        )
    
    try:
        # Simulate flow creation
        new_flow = {
            "id": 123,
            "name": flow_data["name"],
            "status": "active",
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        return success_response(
            "flows.created_successfully",
            data=new_flow
        )
        
    except Exception as e:
        logger.error(f"Error creating flow: {e}")
        raise TranslatedHTTPException(
            status_code=500,
            translation_key="api.internal_error"
        )

@app.get("/api/flows/{flow_id}")
async def get_flow(flow_id: int, request: Request):
    """Get a specific flow with translated error handling"""
    
    # Simulate flow lookup
    if flow_id == 999:  # Simulate not found
        raise TranslatedNotFoundError()
    
    flow = {
        "id": flow_id,
        "name": f"Flow {flow_id}",
        "status": "active"
    }
    
    return success_response(
        "flows.retrieved_successfully",
        data=flow
    )

@app.delete("/api/flows/{flow_id}")
async def delete_flow(flow_id: int, request: Request):
    """Delete a flow with translated confirmation"""
    
    # Check if flow exists
    if flow_id == 999:
        raise TranslatedNotFoundError()
    
    try:
        # Simulate deletion
        logger.info(f"Deleting flow {flow_id}")
        
        return success_response("flows.deleted_successfully")
        
    except Exception as e:
        logger.error(f"Error deleting flow {flow_id}: {e}")
        raise TranslatedHTTPException(
            status_code=500,
            translation_key="api.internal_error"
        )

# Example: User authentication with translation

@app.post("/api/auth/login")
async def login(credentials: Dict[str, str], request: Request):
    """Login endpoint with translated error messages"""
    
    username = credentials.get("username", "").strip()
    password = credentials.get("password", "").strip()
    
    if not username or not password:
        raise TranslatedHTTPException(
            status_code=422,
            translation_key="auth.invalid_credentials"
        )
    
    # Simulate authentication
    if username == "admin" and password == "password":
        return success_response(
            "auth.login_successful",
            data={
                "access_token": "fake_token_123",
                "token_type": "bearer",
                "user": {"username": username, "role": "admin"}
            }
        )
    else:
        raise TranslatedHTTPException(
            status_code=401,
            translation_key="auth.invalid_credentials"
        )

# Example: File upload with translated validation

@app.post("/api/files/upload")
async def upload_file(request: Request):
    """File upload with translated error messages"""
    
    # Simulate file validation
    file_size = 10 * 1024 * 1024  # 10MB
    max_size = 5 * 1024 * 1024    # 5MB limit
    
    if file_size > max_size:
        raise TranslatedHTTPException(
            status_code=413,
            translation_key="api.file_too_large"
        )
    
    # Simulate unsupported file type
    file_type = "exe"
    allowed_types = ["jpg", "png", "pdf", "txt"]
    
    if file_type not in allowed_types:
        raise TranslatedHTTPException(
            status_code=422,
            translation_key="api.invalid_file_type"
        )
    
    return success_response(
        "files.uploaded_successfully",
        data={"file_id": "file_123", "size": file_size}
    )

# Example: Component validation with field-specific errors

@app.post("/api/components/validate")
async def validate_component(component_data: Dict[str, Any], request: Request):
    """Validate component with translated field errors"""
    
    errors = []
    
    # Check required fields
    required_fields = ["name", "type", "inputs", "outputs"]
    for field in required_fields:
        if field not in component_data:
            errors.append({
                "field": field,
                "message": translate_for_request(
                    "components.missing_required_field", 
                    field=field
                )
            })
    
    # Check field values
    if "name" in component_data and len(component_data["name"]) < 2:
        errors.append({
            "field": "name",
            "message": translate_for_request(
                "validation.min_length",
                min=2
            )
        })
    
    if errors:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": translate_for_request("components.validation_failed"),
                "errors": errors
            }
        )
    
    return success_response(
        "components.validation_successful",
        data={"valid": True}
    )

# Health check endpoint with language info

@app.get("/api/health")
async def health_check(request: Request):
    """Health check that shows current language"""
    
    current_lang = get_current_language()
    translation_service = get_translation_service()
    available_languages = translation_service.get_available_locales()
    
    return {
        "status": "healthy",
        "message": translate_for_request("system.startup_complete"),
        "language": {
            "current": current_lang,
            "available": available_languages
        },
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Example middleware for logging requests with language info

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log requests with language information"""
    
    # Get language before processing
    accept_language = request.headers.get("accept-language", "")
    x_language = request.headers.get("x-language", "")
    
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Accept-Language: {accept_language} "
        f"X-Language: {x_language}"
    )
    
    response = await call_next(request)
    
    # Log response with final language
    final_language = get_current_language()
    logger.info(f"Response: {response.status_code} Language: {final_language}")
    
    return response

if __name__ == "__main__":
    import uvicorn
    
    # Start server with translation support
    logger.info("Starting Axiestudio API with i18n support...")
    logger.info(f"Available languages: {get_translation_service().get_available_locales()}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )
