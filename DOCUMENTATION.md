# Adipose Documentation

## Overview

Adipose is a powerful code generation platform that creates production-ready backend and frontend API layers from a single YAML/JSON configuration file. It eliminates boilerplate code and ensures consistency across your entire stack.

## Key Features

### ✨ Core Features
- **Single Source of Truth**: Define your API once in YAML/JSON
- **Multi-Framework Support**: 5 backend + 5 frontend frameworks
- **Type-Safe Code Generation**: Strongly-typed models and API clients
- **Built-in Best Practices**: Authentication, validation, error handling, pagination
- **Industry Standard Libraries**: Uses proven libraries for each platform

### 🔐 Security & Authentication
- JWT token authentication
- OAuth2 support
- API key authentication
- Automatic token management in frontend clients

### ✅ Data Validation
- Request/response validation
- Field-level constraints (min/max length, patterns, ranges)
- Unique constraints
- Foreign key relationships

### 🚀 Performance
- Built-in pagination
- Query filtering and sorting
- Database indexing
- Connection pooling

## Supported Platforms

### Backend Frameworks
1. **Django (Python)** - Django REST Framework
2. **Express.js (Node.js)** - Express with TypeScript
3. **.NET (C#)** - ASP.NET Core
4. **Spring Boot (Java)** - Spring Boot REST
5. **Laravel (PHP)** - Laravel API

### Frontend Frameworks
1. **JavaScript/TypeScript** - Axios-based client
2. **Flutter (Dart)** - Dio HTTP client
3. **Swift (iOS)** - Native URLSession
4. **Kotlin (Android)** - Retrofit/OkHttp
5. **AvaloniaUI (C#)** - HttpClient

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/adipose.git
cd adipose

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Quick Start

### 1. Create Configuration File

Create `my-api.yaml`:

```yaml
project:
  name: MyAPI
  version: 1.0.0
  base_url: https://api.myapp.com

auth:
  type: jwt
  token_header: Authorization
  token_prefix: Bearer

models:
  User:
    fields:
      id: integer
      username: string
      email: string
      password: string
    timestamps: true

endpoints:
  - resource: users
    model: User
    operations: [create, read, update, delete, list]
    auth_required: true
```

### 2. Generate Code

```bash
# Generate Django backend
adipose generate --config my-api.yaml --backend django --output ./backend

# Generate Swift iOS frontend
adipose generate --config my-api.yaml --frontend swift --output ./ios-client

# Generate both at once
adipose generate --config my-api.yaml --backend express --frontend flutter --output ./output
```

### 3. Use Generated Code

**Django Backend:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Express Backend:**
```bash
cd backend
npm install
npm start
```

## Configuration Reference

### Project Configuration

```yaml
project:
  name: MyApp              # Project name (required)
  version: 1.0.0           # API version
  base_url: https://...    # Base URL (required)
  description: My API      # Optional description
```

### Authentication Configuration

```yaml
auth:
  type: jwt                     # jwt, oauth2, api_key, none
  token_header: Authorization   # Header name
  token_prefix: Bearer          # Token prefix
  jwt_secret_env: JWT_SECRET    # Environment variable for secret
  jwt_algorithm: HS256          # JWT algorithm
  jwt_expiry: 3600             # Expiry in seconds
```

### Model Configuration

```yaml
models:
  ModelName:
    fields:
      field_name:
        type: string              # Field type
        required: true            # Required field
        nullable: false           # Can be null
        default: value            # Default value
        min_length: 3            # Min string length
        max_length: 100          # Max string length
        min_value: 0             # Min numeric value
        max_value: 999           # Max numeric value
        pattern: "^[a-z]+$"      # Regex pattern
        unique: true             # Unique constraint
        index: true              # Create index
        foreign_key: OtherModel  # Foreign key reference
    table_name: custom_table     # Custom table name
    timestamps: true             # Add created_at/updated_at
    soft_delete: false           # Enable soft delete
```

### Field Types

- `integer` - Integer number
- `float` - Floating point number
- `string` - Short text (VARCHAR)
- `text` - Long text (TEXT)
- `boolean` - True/False
- `datetime` - Date and time
- `date` - Date only
- `json` - JSON object
- `array` - Array/List

### Endpoint Configuration

```yaml
endpoints:
  - resource: users              # Resource name
    model: User                  # Associated model
    operations:                  # Allowed operations
      - create                   # POST /users
      - read                     # GET /users/{id}
      - update                   # PUT /users/{id}
      - delete                   # DELETE /users/{id}
      - list                     # GET /users
      - search                   # GET /users/search
    auth_required: true          # Require authentication
    pagination: true             # Enable pagination
    page_size: 20               # Default page size
    max_page_size: 100          # Maximum page size
    filters:                     # Filterable fields
      - username
      - email
    sort_fields:                 # Sortable fields
      - username
      - created_at
```

### Database Configuration

```yaml
database:
  type: postgresql              # postgresql, mysql, sqlite, mongodb
  host_env: DB_HOST            # Environment variables
  port_env: DB_PORT
  name_env: DB_NAME
  user_env: DB_USER
  password_env: DB_PASSWORD
  migrations: true             # Generate migrations
```

### CORS Configuration

```yaml
cors:
  enabled: true
  origins: ["*"]               # Allowed origins
  methods: [GET, POST, PUT]    # Allowed methods
  headers: ["*"]               # Allowed headers
  credentials: true            # Allow credentials
  max_age: 3600               # Preflight cache duration
```

### Error Handling Configuration

```yaml
error_handling:
  format: standard             # standard, rfc7807, custom
  include_stack_trace: false   # Include stack traces
  log_errors: true            # Log errors
```

## CLI Commands

### Generate Code
```bash
adipose generate --config <file> --backend <framework> --frontend <framework> --output <dir>

# Examples
adipose generate -c api.yaml -b django -o ./output
adipose generate -c api.yaml -f swift -o ./ios-client
adipose generate -c api.yaml -b express -f flutter -o ./fullstack
```

### Validate Configuration
```bash
adipose validate --config <file>

# Example
adipose validate -c api.yaml
```

### List Platforms
```bash
adipose list-platforms
```

### Generate Example Config
```bash
adipose init --output api-config.yaml
```

## Generated Code Structure

### Django Backend
```
backend/
├── manage.py
├── requirements.txt
├── BlogAPI/
│   ├── settings.py
│   └── urls.py
└── api/
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   └── post.py
    ├── serializers/
    │   ├── user.py
    │   └── post.py
    ├── views/
    │   ├── users.py
    │   └── posts.py
    ├── authentication.py
    └── middleware.py
```

### Express Backend
```
backend/
├── package.json
├── src/
│   ├── server.js
│   ├── models/
│   ├── routes/
│   ├── controllers/
│   ├── middleware/
│   └── config/
└── .env.example
```

### TypeScript Frontend
```
frontend/
├── package.json
├── src/
│   ├── api/
│   │   └── client.ts
│   ├── models/
│   │   ├── User.ts
│   │   └── Post.ts
│   ├── services/
│   │   ├── usersService.ts
│   │   └── postsService.ts
│   ├── auth/
│   │   └── AuthManager.ts
│   └── config/
│       └── api.config.ts
```

## Examples

See the `examples/` directory for complete working examples:

- `examples/blog-api.yaml` - Blog API configuration
- `examples/ecommerce-api.yaml` - E-commerce API configuration
- `examples/output/` - Generated code samples

## Advanced Usage

### Custom Endpoints

Add custom endpoints beyond CRUD:

```yaml
endpoints:
  - resource: users
    model: User
    operations: [create, read, update, delete, list]
    custom_endpoints:
      - name: activate
        method: POST
        path: /users/{id}/activate
      - name: reset-password
        method: POST
        path: /users/reset-password
```

### Environment Variables

All generated backends support environment-based configuration:

```bash
# .env file
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=secret
JWT_SECRET=your-secret-key
```

## Best Practices

1. **Version Control**: Keep your configuration file in version control
2. **Environment Secrets**: Never commit secrets; use environment variables
3. **Validation**: Always validate your config before generating code
4. **Iterative Development**: Regenerate code as your API evolves
5. **Custom Code**: Add custom logic in separate files to avoid overwriting

## Troubleshooting

### Configuration Validation Errors
```bash
adipose validate --config your-config.yaml
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Template Errors
Check that all templates exist in `adipose/templates/`

## Contributing

Contributions are welcome! To add a new backend or frontend generator:

1. Create generator class in `adipose/generators/backend/` or `frontend/`
2. Inherit from `CodeGenerator` base class
3. Implement the `generate()` method
4. Create Jinja2 templates in `adipose/templates/`
5. Register in `adipose/cli/main.py`

## License

MIT License - see LICENSE file

## Support

- GitHub Issues: https://github.com/yourusername/adipose/issues
- Documentation: https://adipose.readthedocs.io
- Email: support@adipose.dev
