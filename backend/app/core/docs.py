"""
OpenAPI documentation configuration and customization.
"""
from typing import Dict, Any

from .settings import settings


def get_openapi_config() -> Dict[str, Any]:
    """Get OpenAPI configuration for FastAPI."""
    return {
        "title": settings.name,
        "version": settings.version,
        "description": """
        Modern FastAPI Backend Service

        ## Features
        - JWT Authentication
        - Rate Limiting
        - Background Jobs
        - Structured Logging
        - Comprehensive Error Handling

        ## Authentication
        Use the `/v1/auth/login` endpoint to obtain an access token.
        Include the token in the Authorization header: `Bearer <token>`
        """,
        "contact": {
            "name": "API Support",
            "email": "alexypoloz@gmail.com",
        },
        "license_info": {
            "name": "MIT",
        },
        "servers": [
            {
                "url": f"http://localhost:{settings.port}",
                "description": "Development server"
            },
        ] if settings.env == "dev" else [],
    }


def get_openapi_tags() -> list:
    """Define OpenAPI tags for endpoint grouping."""
    return [
        {
            "name": "auth",
            "description": "Authentication endpoints"
        },
        {
            "name": "users",
            "description": "User management operations"
        },
        {
            "name": "posts",
            "description": "Post management operations"
        },
        {
            "name": "billing",
            "description": "Billing and payment operations"
        },
        {
            "name": "admin",
            "description": "Administrative operations"
        },
        {
            "name": "system",
            "description": "System monitoring and health checks"
        },
    ]