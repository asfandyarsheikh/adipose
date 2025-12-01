# Adipose

Generate production-ready backend and frontend API layers from a single configuration file.

## Overview

Adipose is a powerful code generation platform that creates complete API layers with serialization, validation, authentication, error handling, and data management for multiple backend and frontend frameworks from a single YAML/JSON configuration.

## Supported Platforms

### Backend
- **Express.js** (Node.js)
- **Django** (Python)
- **.NET** (C#)
- **Spring Boot** (Java)
- **Laravel** (PHP)

### Frontend
- **JavaScript** (Axios/Fetch)
- **Flutter** (Dart)
- **Swift** (iOS Native)
- **Kotlin** (Android Native)
- **AvaloniaUI** (C#)

## Features

- 🚀 **Quick Setup**: Generate complete API layers in seconds
- ✅ **Type-Safe**: Generates strongly-typed models and API clients
- 🔐 **Authentication**: JWT, OAuth2, API Key support built-in
- ⚡ **Validation**: Automatic request/response validation
- 🎯 **Error Handling**: Standardized error responses across all platforms
- 📦 **Serialization**: JSON serialization/deserialization handled automatically
- 🔄 **CRUD Operations**: Standard Create, Read, Update, Delete operations
- 📝 **Documentation**: Auto-generated API documentation

## Installation

```bash
pip install -e .
```

## Quick Start

1. Create a configuration file `api-config.yaml`:

```yaml
project:
  name: MyApp
  version: 1.0.0
  base_url: https://api.myapp.com

auth:
  type: jwt
  token_header: Authorization

models:
  User:
    fields:
      id: integer
      username: string
      email: string
      created_at: datetime
    
  Post:
    fields:
      id: integer
      title: string
      content: text
      user_id: integer
      published: boolean

endpoints:
  - resource: users
    model: User
    operations: [create, read, update, delete, list]
    auth_required: true
    
  - resource: posts
    model: Post
    operations: [create, read, update, delete, list]
    auth_required: true
```

2. Generate code:

```bash
# Generate backend
adipose generate --config api-config.yaml --backend express --output ./backend

# Generate frontend
adipose generate --config api-config.yaml --frontend swift --output ./ios-client

# Generate both
adipose generate --config api-config.yaml --backend django --frontend flutter --output ./output
```

## CLI Commands

```bash
# Generate code
adipose generate --config <config-file> --backend <backend> --frontend <frontend> --output <dir>

# Validate configuration
adipose validate --config <config-file>

# List supported platforms
adipose list-platforms

# Generate example config
adipose init --output api-config.yaml
```

## Configuration Schema

See the full documentation for detailed configuration options.

## License

MIT
