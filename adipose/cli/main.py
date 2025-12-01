"""CLI interface for Adipose."""

import click
import sys
from pathlib import Path
from typing import Optional

from adipose.core.generator import load_config, validate_config
from adipose.generators.backend.django_generator import DjangoGenerator
from adipose.generators.backend.express_generator import ExpressGenerator
from adipose.generators.backend.dotnet_generator import DotNetGenerator
from adipose.generators.backend.springboot_generator import SpringBootGenerator
from adipose.generators.backend.laravel_generator import LaravelGenerator
from adipose.generators.frontend.javascript_generator import JavaScriptGenerator
from adipose.generators.frontend.flutter_generator import FlutterGenerator
from adipose.generators.frontend.swift_generator import SwiftGenerator
from adipose.generators.frontend.kotlin_generator import KotlinGenerator
from adipose.generators.frontend.avaloniaui_generator import AvaloniaUIGenerator


BACKEND_GENERATORS = {
    'django': DjangoGenerator,
    'express': ExpressGenerator,
    'dotnet': DotNetGenerator,
    'springboot': SpringBootGenerator,
    'laravel': LaravelGenerator,
}

FRONTEND_GENERATORS = {
    'javascript': JavaScriptGenerator,
    'typescript': JavaScriptGenerator,
    'flutter': FlutterGenerator,
    'swift': SwiftGenerator,
    'kotlin': KotlinGenerator,
    'avaloniaui': AvaloniaUIGenerator,
}


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Adipose - Generate backend and frontend API layers from a single config."""
    pass


@cli.command()
@click.option('--config', '-c', required=True, type=click.Path(exists=True), help='Configuration file path')
@click.option('--backend', '-b', type=click.Choice(list(BACKEND_GENERATORS.keys())), help='Backend framework')
@click.option('--frontend', '-f', type=click.Choice(list(FRONTEND_GENERATORS.keys())), help='Frontend framework')
@click.option('--output', '-o', required=True, type=click.Path(), help='Output directory')
def generate(config: str, backend: Optional[str], frontend: Optional[str], output: str):
    """Generate code from configuration."""
    
    if not backend and not frontend:
        click.echo("Error: Specify at least --backend or --frontend", err=True)
        sys.exit(1)
    
    try:
        # Load and validate config
        click.echo(f"Loading configuration from {config}...")
        api_config = load_config(config)
        click.echo("✓ Configuration loaded successfully\n")
        
        # Generate backend
        if backend:
            backend_output = Path(output) / 'backend'
            click.echo(f"Generating {backend} backend to {backend_output}...")
            generator_class = BACKEND_GENERATORS[backend]
            generator = generator_class(api_config, str(backend_output))
            generator.generate()
        
        # Generate frontend
        if frontend:
            frontend_output = Path(output) / 'frontend'
            click.echo(f"\nGenerating {frontend} frontend to {frontend_output}...")
            generator_class = FRONTEND_GENERATORS[frontend]
            generator = generator_class(api_config, str(frontend_output))
            generator.generate()
        
        click.echo("\n✓ Code generation complete!")
        click.echo(f"\nOutput directory: {output}")
        
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--config', '-c', required=True, type=click.Path(exists=True), help='Configuration file path')
def validate(config: str):
    """Validate configuration file."""
    try:
        validate_config(config)
    except Exception as e:
        click.echo(f"✗ Validation failed: {str(e)}", err=True)
        sys.exit(1)


@cli.command('list-platforms')
def list_platforms():
    """List supported backend and frontend platforms."""
    click.echo("\n=== Supported Platforms ===\n")
    
    click.echo("Backend:")
    for platform in BACKEND_GENERATORS.keys():
        click.echo(f"  • {platform}")
    
    click.echo("\nFrontend:")
    for platform in FRONTEND_GENERATORS.keys():
        click.echo(f"  • {platform}")
    click.echo()


@cli.command()
@click.option('--output', '-o', default='api-config.yaml', type=click.Path(), help='Output file path')
def init(output: str):
    """Generate example configuration file."""
    example_config = """project:
  name: MyApp
  version: 1.0.0
  base_url: https://api.myapp.com
  description: My awesome API

auth:
  type: jwt
  token_header: Authorization
  token_prefix: Bearer
  jwt_secret_env: JWT_SECRET
  jwt_algorithm: HS256
  jwt_expiry: 3600

models:
  User:
    fields:
      id:
        type: integer
        required: true
      username:
        type: string
        required: true
        min_length: 3
        max_length: 50
        unique: true
      email:
        type: string
        required: true
        pattern: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\\\.[a-zA-Z0-9-.]+$'
        unique: true
      password:
        type: string
        required: true
        min_length: 8
      created_at:
        type: datetime
        required: false
    timestamps: true
    
  Post:
    fields:
      id:
        type: integer
        required: true
      title:
        type: string
        required: true
        max_length: 200
      content:
        type: text
        required: true
      user_id:
        type: integer
        required: true
        foreign_key: User
      published:
        type: boolean
        default: false
      created_at:
        type: datetime
    timestamps: true

endpoints:
  - resource: users
    model: User
    operations: [create, read, update, delete, list]
    auth_required: true
    pagination: true
    page_size: 20
    filters: [username, email]
    sort_fields: [username, created_at]
    
  - resource: posts
    model: Post
    operations: [create, read, update, delete, list, search]
    auth_required: true
    pagination: true
    page_size: 20
    filters: [user_id, published]
    sort_fields: [title, created_at]

database:
  type: postgresql
  host_env: DB_HOST
  port_env: DB_PORT
  name_env: DB_NAME
  user_env: DB_USER
  password_env: DB_PASSWORD
  migrations: true

cors:
  enabled: true
  origins: ["*"]
  methods: [GET, POST, PUT, DELETE, PATCH, OPTIONS]
  headers: ["*"]
  credentials: true

error_handling:
  format: standard
  include_stack_trace: false
  log_errors: true
"""
    
    try:
        with open(output, 'w') as f:
            f.write(example_config)
        click.echo(f"✓ Example configuration created: {output}")
        click.echo("\nEdit this file and run:")
        click.echo(f"  adipose generate --config {output} --backend django --output ./output")
    except Exception as e:
        click.echo(f"✗ Error creating config: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
