"""Core code generation engine for Adipose."""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

from adipose.schemas.config import APIConfig


class CodeGenerator:
    """Base code generator class."""
    
    def __init__(self, config: APIConfig, output_dir: str):
        """Initialize code generator.
        
        Args:
            config: API configuration
            output_dir: Output directory for generated code
        """
        self.config = config
        self.output_dir = Path(output_dir)
        self.templates_dir = Path(__file__).parent.parent / "templates"
        
        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Add custom filters
        self._setup_jinja_filters()
    
    def _setup_jinja_filters(self):
        """Setup custom Jinja2 filters."""
        from adipose.utils.helpers import (
            to_snake_case, to_camel_case, to_pascal_case, to_kebab_case,
            pluralize, singularize, type_mapping, get_http_method, get_endpoint_path
        )
        
        self.jinja_env.filters['snake_case'] = to_snake_case
        self.jinja_env.filters['camel_case'] = to_camel_case
        self.jinja_env.filters['pascal_case'] = to_pascal_case
        self.jinja_env.filters['kebab_case'] = to_kebab_case
        self.jinja_env.filters['pluralize'] = pluralize
        self.jinja_env.filters['singularize'] = singularize
        self.jinja_env.filters['type_map'] = type_mapping
        self.jinja_env.filters['http_method'] = get_http_method
        self.jinja_env.filters['endpoint_path'] = get_endpoint_path
    
    def generate(self):
        """Generate code. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement generate()")
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a Jinja2 template.
        
        Args:
            template_name: Name of the template file
            context: Template context variables
            
        Returns:
            Rendered template string
        """
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)
    
    def write_file(self, relative_path: str, content: str):
        """Write content to a file.
        
        Args:
            relative_path: Relative path from output directory
            content: File content
        """
        file_path = self.output_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Generated: {relative_path}")
    
    def copy_template_file(self, template_path: str, output_path: str):
        """Copy a template file to output directory.
        
        Args:
            template_path: Path to template file relative to templates directory
            output_path: Output path relative to output directory
        """
        source = self.templates_dir / template_path
        destination = self.output_dir / output_path
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        if source.exists():
            import shutil
            shutil.copy2(source, destination)
            print(f"Copied: {output_path}")
    
    def get_context(self) -> Dict[str, Any]:
        """Get common template context.
        
        Returns:
            Dictionary with common context variables
        """
        return {
            'config': self.config,
            'project': self.config.project,
            'auth': self.config.auth,
            'models': self.config.models,
            'endpoints': self.config.endpoints,
            'database': self.config.database,
            'cors': self.config.cors,
            'error_handling': self.config.error_handling,
        }


def load_config(config_path: str) -> APIConfig:
    """Load API configuration from file.
    
    Args:
        config_path: Path to configuration file (YAML or JSON)
        
    Returns:
        Parsed API configuration
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        if config_path.endswith('.json'):
            data = json.load(f)
        else:
            data = yaml.safe_load(f)
    
    return APIConfig(**data)


def validate_config(config_path: str) -> bool:
    """Validate configuration file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        True if valid, raises exception otherwise
    """
    try:
        load_config(config_path)
        print(f"✓ Configuration valid: {config_path}")
        return True
    except Exception as e:
        print(f"✗ Configuration invalid: {str(e)}")
        raise
