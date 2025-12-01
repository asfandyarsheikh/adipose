"""Configuration schema for Adipose API generator."""

from typing import Dict, List, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator


class ProjectConfig(BaseModel):
    """Project metadata configuration."""
    name: str = Field(..., description="Project name")
    version: str = Field(default="1.0.0", description="Project version")
    base_url: str = Field(..., description="Base API URL")
    description: Optional[str] = Field(None, description="Project description")


class AuthConfig(BaseModel):
    """Authentication configuration."""
    type: Literal["jwt", "oauth2", "api_key", "none"] = Field(
        default="jwt", description="Authentication type"
    )
    token_header: str = Field(default="Authorization", description="Authorization header name")
    token_prefix: Optional[str] = Field(default="Bearer", description="Token prefix (e.g., 'Bearer')")
    
    # JWT specific
    jwt_secret_env: Optional[str] = Field(default="JWT_SECRET", description="Environment variable for JWT secret")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiry: int = Field(default=3600, description="JWT expiry in seconds")
    
    # OAuth2 specific
    oauth2_provider: Optional[str] = Field(None, description="OAuth2 provider")
    oauth2_scopes: Optional[List[str]] = Field(default=None, description="OAuth2 scopes")
    
    # API Key specific
    api_key_header: Optional[str] = Field(default="X-API-Key", description="API key header name")


class FieldConfig(BaseModel):
    """Model field configuration."""
    type: str = Field(..., description="Field type (string, integer, float, boolean, datetime, text, etc.)")
    required: bool = Field(default=True, description="Whether field is required")
    nullable: bool = Field(default=False, description="Whether field can be null")
    default: Optional[Any] = Field(None, description="Default value")
    description: Optional[str] = Field(None, description="Field description")
    min_length: Optional[int] = Field(None, description="Minimum length for strings")
    max_length: Optional[int] = Field(None, description="Maximum length for strings")
    min_value: Optional[float] = Field(None, description="Minimum value for numbers")
    max_value: Optional[float] = Field(None, description="Maximum value for numbers")
    pattern: Optional[str] = Field(None, description="Regex pattern for validation")
    foreign_key: Optional[str] = Field(None, description="Foreign key reference (e.g., 'User')")
    unique: bool = Field(default=False, description="Whether field must be unique")
    index: bool = Field(default=False, description="Whether to create database index")


class ModelConfig(BaseModel):
    """Data model configuration."""
    fields: Dict[str, Any] = Field(..., description="Model fields")
    table_name: Optional[str] = Field(None, description="Custom table name")
    description: Optional[str] = Field(None, description="Model description")
    timestamps: bool = Field(default=True, description="Add created_at/updated_at fields")
    soft_delete: bool = Field(default=False, description="Enable soft delete")
    
    @field_validator("fields", mode="before")
    @classmethod
    def parse_fields(cls, v):
        """Parse field definitions."""
        if isinstance(v, dict):
            parsed = {}
            for field_name, field_def in v.items():
                if isinstance(field_def, str):
                    # Simple string type definition
                    parsed[field_name] = FieldConfig(type=field_def)
                elif isinstance(field_def, dict):
                    # Full field configuration
                    parsed[field_name] = FieldConfig(**field_def)
                else:
                    parsed[field_name] = field_def
            return parsed
        return v


class EndpointConfig(BaseModel):
    """API endpoint configuration."""
    resource: str = Field(..., description="Resource name (e.g., 'users')")
    model: str = Field(..., description="Associated model name")
    operations: List[Literal["create", "read", "update", "delete", "list", "search"]] = Field(
        default=["list", "read", "create", "update", "delete"],
        description="Allowed operations"
    )
    auth_required: bool = Field(default=True, description="Whether authentication is required")
    rate_limit: Optional[int] = Field(None, description="Rate limit per minute")
    custom_endpoints: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Custom endpoint definitions"
    )
    pagination: bool = Field(default=True, description="Enable pagination for list operations")
    page_size: int = Field(default=20, description="Default page size")
    max_page_size: int = Field(default=100, description="Maximum page size")
    filters: Optional[List[str]] = Field(default=None, description="Fields that can be filtered")
    sort_fields: Optional[List[str]] = Field(default=None, description="Fields that can be sorted")


class DatabaseConfig(BaseModel):
    """Database configuration."""
    type: Literal["postgresql", "mysql", "sqlite", "mongodb", "sqlserver"] = Field(
        default="postgresql", description="Database type"
    )
    host_env: str = Field(default="DB_HOST", description="Environment variable for database host")
    port_env: str = Field(default="DB_PORT", description="Environment variable for database port")
    name_env: str = Field(default="DB_NAME", description="Environment variable for database name")
    user_env: str = Field(default="DB_USER", description="Environment variable for database user")
    password_env: str = Field(default="DB_PASSWORD", description="Environment variable for database password")
    migrations: bool = Field(default=True, description="Generate database migrations")


class ErrorHandlingConfig(BaseModel):
    """Error handling configuration."""
    format: Literal["standard", "rfc7807", "custom"] = Field(
        default="standard", description="Error response format"
    )
    include_stack_trace: bool = Field(default=False, description="Include stack traces in development")
    log_errors: bool = Field(default=True, description="Log errors")
    custom_errors: Optional[Dict[str, Any]] = Field(default=None, description="Custom error definitions")


class CorsConfig(BaseModel):
    """CORS configuration."""
    enabled: bool = Field(default=True, description="Enable CORS")
    origins: List[str] = Field(default=["*"], description="Allowed origins")
    methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        description="Allowed methods"
    )
    headers: List[str] = Field(default=["*"], description="Allowed headers")
    credentials: bool = Field(default=True, description="Allow credentials")
    max_age: int = Field(default=3600, description="Preflight cache duration in seconds")


class APIConfig(BaseModel):
    """Complete API configuration."""
    project: ProjectConfig = Field(..., description="Project configuration")
    auth: AuthConfig = Field(default_factory=AuthConfig, description="Authentication configuration")
    models: Dict[str, ModelConfig] = Field(..., description="Data models")
    endpoints: List[EndpointConfig] = Field(..., description="API endpoints")
    database: Optional[DatabaseConfig] = Field(
        default_factory=DatabaseConfig, description="Database configuration"
    )
    error_handling: ErrorHandlingConfig = Field(
        default_factory=ErrorHandlingConfig, description="Error handling configuration"
    )
    cors: CorsConfig = Field(default_factory=CorsConfig, description="CORS configuration")
    
    @field_validator("models", mode="before")
    @classmethod
    def parse_models(cls, v):
        """Parse model definitions."""
        if isinstance(v, dict):
            parsed = {}
            for model_name, model_def in v.items():
                if isinstance(model_def, dict):
                    parsed[model_name] = ModelConfig(**model_def)
                else:
                    parsed[model_name] = model_def
            return parsed
        return v
