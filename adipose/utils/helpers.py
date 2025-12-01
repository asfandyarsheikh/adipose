"""Utility functions for Adipose."""

import re
import inflection
from typing import Dict, Any


def to_snake_case(name: str) -> str:
    """Convert string to snake_case."""
    return inflection.underscore(name)


def to_camel_case(name: str) -> str:
    """Convert string to camelCase."""
    return inflection.camelize(name, uppercase_first_letter=False)


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase."""
    return inflection.camelize(name, uppercase_first_letter=True)


def to_kebab_case(name: str) -> str:
    """Convert string to kebab-case."""
    return inflection.dasherize(inflection.underscore(name))


def pluralize(name: str) -> str:
    """Pluralize a word."""
    return inflection.pluralize(name)


def singularize(name: str) -> str:
    """Singularize a word."""
    return inflection.singularize(name)


def type_mapping(field_type: str, target_lang: str) -> str:
    """Map generic field types to target language types."""
    
    type_maps = {
        "python": {
            "string": "str",
            "integer": "int",
            "float": "float",
            "boolean": "bool",
            "datetime": "datetime",
            "date": "date",
            "text": "str",
            "json": "dict",
            "array": "list",
        },
        "typescript": {
            "string": "string",
            "integer": "number",
            "float": "number",
            "boolean": "boolean",
            "datetime": "Date",
            "date": "Date",
            "text": "string",
            "json": "any",
            "array": "Array<any>",
        },
        "java": {
            "string": "String",
            "integer": "Integer",
            "float": "Double",
            "boolean": "Boolean",
            "datetime": "LocalDateTime",
            "date": "LocalDate",
            "text": "String",
            "json": "JsonNode",
            "array": "List<Object>",
        },
        "csharp": {
            "string": "string",
            "integer": "int",
            "float": "double",
            "boolean": "bool",
            "datetime": "DateTime",
            "date": "DateTime",
            "text": "string",
            "json": "JsonElement",
            "array": "List<object>",
        },
        "php": {
            "string": "string",
            "integer": "int",
            "float": "float",
            "boolean": "bool",
            "datetime": "\\DateTime",
            "date": "\\DateTime",
            "text": "string",
            "json": "array",
            "array": "array",
        },
        "swift": {
            "string": "String",
            "integer": "Int",
            "float": "Double",
            "boolean": "Bool",
            "datetime": "Date",
            "date": "Date",
            "text": "String",
            "json": "[String: Any]",
            "array": "[Any]",
        },
        "kotlin": {
            "string": "String",
            "integer": "Int",
            "float": "Double",
            "boolean": "Boolean",
            "datetime": "LocalDateTime",
            "date": "LocalDate",
            "text": "String",
            "json": "JsonObject",
            "array": "List<Any>",
        },
        "dart": {
            "string": "String",
            "integer": "int",
            "float": "double",
            "boolean": "bool",
            "datetime": "DateTime",
            "date": "DateTime",
            "text": "String",
            "json": "Map<String, dynamic>",
            "array": "List<dynamic>",
        },
    }
    
    return type_maps.get(target_lang, {}).get(field_type.lower(), field_type)


def get_http_method(operation: str) -> str:
    """Get HTTP method for operation."""
    method_map = {
        "create": "POST",
        "read": "GET",
        "list": "GET",
        "update": "PUT",
        "delete": "DELETE",
        "search": "GET",
        "patch": "PATCH",
    }
    return method_map.get(operation, "GET")


def get_endpoint_path(resource: str, operation: str, with_id: bool = False) -> str:
    """Generate endpoint path."""
    base = f"/{resource}"
    
    if operation in ["read", "update", "delete"]:
        return f"{base}/{{id}}"
    elif operation == "search":
        return f"{base}/search"
    else:
        return base


def sanitize_identifier(name: str) -> str:
    """Sanitize identifier to be valid in most languages."""
    # Remove special characters except underscore
    sanitized = re.sub(r'[^\w]', '_', name)
    # Ensure it doesn't start with a number
    if sanitized[0].isdigit():
        sanitized = f"_{sanitized}"
    return sanitized


def generate_example_value(field_type: str) -> Any:
    """Generate example value for a field type."""
    examples = {
        "string": "example_string",
        "integer": 1,
        "float": 1.0,
        "boolean": True,
        "datetime": "2024-01-01T00:00:00Z",
        "date": "2024-01-01",
        "text": "Example text content",
        "json": {},
        "array": [],
    }
    return examples.get(field_type.lower(), None)
