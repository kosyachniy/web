#!/usr/bin/env python3
"""
Generate OpenAPI Schema

Script to generate clean OpenAPI schema from FastAPI application.
This is TDD Step 3 from CLAUDE.md workflow.
"""

from __future__ import annotations

import json
import asyncio
from pathlib import Path

from app.main import create_app
from app.core.config import get_settings
from app.core.container import container, wire_container


async def generate_openapi_schema():
    """Generate OpenAPI schema with proper configuration."""
    print("🔧 Generating OpenAPI schema...")

    # Initialize application
    settings = get_settings()
    container.config.from_pydantic(settings)
    wire_container()

    # Create app instance
    app = create_app()

    # Generate OpenAPI schema
    openapi_schema = app.openapi()

    # Ensure clean schema format
    if openapi_schema:
        # Add additional metadata
        openapi_schema["info"]["title"] = "Modern Backend API"
        openapi_schema["info"]["description"] = "Scalable backend with hexagonal architecture"
        openapi_schema["info"]["version"] = "1.0.0"
        openapi_schema["info"]["contact"] = {
            "name": "API Support",
            "email": "api-support@example.com"
        }

        # Add servers information
        openapi_schema["servers"] = [
            {
                "url": "http://localhost/api",
                "description": "Local development server"
            },
            {
                "url": "https://api.example.com",
                "description": "Production server"
            }
        ]

        print("✅ OpenAPI schema generated successfully")
        print(f"   - Endpoints: {len(openapi_schema.get('paths', {}))}")
        print(f"   - Schemas: {len(openapi_schema.get('components', {}).get('schemas', {}))}")

        return openapi_schema
    else:
        print("❌ Failed to generate OpenAPI schema")
        return None


async def save_openapi_schema(schema: dict):
    """Save OpenAPI schema to file."""
    # Create output directory
    output_dir = Path(__file__).parent.parent / "generated"
    output_dir.mkdir(exist_ok=True)

    # Save JSON schema
    schema_file = output_dir / "openapi.json"
    with open(schema_file, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    print(f"💾 OpenAPI schema saved to: {schema_file}")

    # Also save to frontend directory if it exists
    frontend_dir = Path(__file__).parent.parent.parent / "frontend" / "generated"
    if frontend_dir.parent.exists():
        frontend_dir.mkdir(exist_ok=True)
        frontend_schema_file = frontend_dir / "openapi.json"

        with open(frontend_schema_file, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)

        print(f"💾 OpenAPI schema also saved to: {frontend_schema_file}")

        return frontend_schema_file

    return schema_file


def validate_openapi_schema(schema: dict) -> bool:
    """Validate OpenAPI schema quality."""
    print("🔍 Validating OpenAPI schema quality...")

    issues = []

    # Check required sections
    required_sections = ["info", "paths", "components"]
    for section in required_sections:
        if section not in schema:
            issues.append(f"Missing required section: {section}")

    # Check paths
    paths = schema.get("paths", {})
    if not paths:
        issues.append("No API paths defined")

    # Check for proper response models
    for path, methods in paths.items():
        for method, details in methods.items():
            if method == "parameters":  # Skip parameters
                continue

            responses = details.get("responses", {})
            if "200" in responses or "201" in responses:
                success_response = responses.get("200") or responses.get("201")
                if "content" in success_response:
                    content = success_response["content"]
                    if "application/json" in content:
                        json_content = content["application/json"]
                        if "schema" not in json_content:
                            issues.append(f"{method.upper()} {path}: Missing response schema")

    # Check schemas
    schemas = schema.get("components", {}).get("schemas", {})
    if not schemas:
        issues.append("No component schemas defined")

    # Check for proper field descriptions in schemas
    schema_issues = []
    for schema_name, schema_def in schemas.items():
        if "properties" in schema_def:
            properties = schema_def["properties"]
            for prop_name, prop_def in properties.items():
                if "description" not in prop_def and "title" not in prop_def:
                    schema_issues.append(f"{schema_name}.{prop_name} missing description")

    if schema_issues:
        if len(schema_issues) > 5:
            issues.append(f"Multiple schema properties missing descriptions ({len(schema_issues)} total)")
        else:
            issues.extend(schema_issues)

    # Report results
    if issues:
        print("⚠️  Schema quality issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Schema quality validation passed")
        return True


async def main():
    """Main function to generate and validate OpenAPI schema."""
    print("🚀 Starting OpenAPI schema generation...")

    try:
        # Generate schema
        schema = await generate_openapi_schema()
        if not schema:
            print("❌ Schema generation failed")
            return False

        # Save schema
        schema_file = await save_openapi_schema(schema)

        # Validate schema quality
        is_valid = validate_openapi_schema(schema)

        if is_valid:
            print("\n🎉 OpenAPI schema generation completed successfully!")
            print(f"   📄 Schema file: {schema_file}")
            print("   🔧 Ready for TypeScript generation")
            return True
        else:
            print("\n⚠️  OpenAPI schema generated with quality issues")
            print("   📄 Schema file created but may need improvements")
            return False

    except Exception as e:
        print(f"❌ Error generating OpenAPI schema: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)