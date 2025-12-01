# Adipose Quick Start Guide

**Generate production-ready backend and frontend API layers from a single config file!**

## What is Adipose?

Adipose is a code generation tool that creates complete, production-ready API layers for multiple frameworks from a single YAML configuration. No more boilerplate code!

### Supported Platforms

**Backends:** Django, Express.js, .NET, Spring Boot, Laravel  
**Frontends:** JavaScript/TypeScript, Flutter, Swift, Kotlin, AvaloniaUI

## Installation

### Option 1: Standalone Executable (No Python Required)

Download the executable for your platform from [Releases](https://github.com/yourusername/adipose/releases):

```bash
# Linux
wget https://github.com/yourusername/adipose/releases/download/v0.1.0/adipose-Linux-x86_64-v0.1.0.tar.gz
tar -xzf adipose-Linux-x86_64-v0.1.0.tar.gz
cd adipose-Linux-x86_64-v0.1.0
./adipose --help

# macOS
curl -L https://github.com/yourusername/adipose/releases/download/v0.1.0/adipose-Darwin-x86_64-v0.1.0.tar.gz | tar xz
cd adipose-Darwin-x86_64-v0.1.0
./adipose --help

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://github.com/yourusername/adipose/releases/download/v0.1.0/adipose-Windows-x86_64-v0.1.0.zip" -OutFile adipose.zip
Expand-Archive adipose.zip
cd adipose
.\adipose.exe --help
```

### Option 2: Install from Source (Python Required)

```bash
git clone https://github.com/yourusername/adipose.git
cd adipose
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
adipose --help
```

## 5-Minute Quick Start

### 1. Create Your API Configuration

Create `blog-api.yaml`:

```yaml
project:
  name: BlogAPI
  version: 1.0.0
  base_url: https://api.myblog.com

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
    
  Post:
    fields:
      id: integer
      title: string
      content: text
      user_id: integer
      published: boolean
    timestamps: true

endpoints:
  - resource: users
    model: User
    operations: [create, read, update, delete, list]
    auth_required: true
    
  - resource: posts
    model: Post
    operations: [create, read, update, delete, list]
    auth_required: true
    pagination: true
    filters: [user_id, published]
```

### 2. Generate Your Code

```bash
# Generate Django backend
adipose generate --config blog-api.yaml --backend django --output ./backend

# Or generate Swift iOS frontend
adipose generate --config blog-api.yaml --frontend swift --output ./ios-client

# Or both!
adipose generate --config blog-api.yaml --backend express --frontend flutter --output ./fullstack
```

### 3. Run Your Generated Backend

**Django:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Your API is now running at http://localhost:8000/api/

**Express:**
```bash
cd backend
npm install
npm start
```

Your API is now running at http://localhost:3000/api/

## Common Commands

```bash
# List all supported platforms
adipose list-platforms

# Create example configuration
adipose init --output my-api.yaml

# Validate your configuration
adipose validate --config my-api.yaml

# Generate specific framework
adipose generate -c my-api.yaml -b django -o ./django-backend
adipose generate -c my-api.yaml -b express -o ./express-backend
adipose generate -c my-api.yaml -b dotnet -o ./dotnet-backend
adipose generate -c my-api.yaml -b springboot -o ./springboot-backend
adipose generate -c my-api.yaml -b laravel -o ./laravel-backend

# Generate frontend clients
adipose generate -c my-api.yaml -f javascript -o ./js-client
adipose generate -c my-api.yaml -f flutter -o ./flutter-app
adipose generate -c my-api.yaml -f swift -o ./ios-app
adipose generate -c my-api.yaml -f kotlin -o ./android-app
```

## What Gets Generated?

### Django Backend (Python)
✅ Models with validation  
✅ Serializers  
✅ ViewSets with CRUD operations  
✅ JWT Authentication  
✅ URL routing  
✅ CORS middleware  
✅ Error handling  
✅ Pagination & filtering  
✅ Database configuration  
✅ requirements.txt  

### Express Backend (Node.js)
✅ TypeScript models  
✅ Controllers  
✅ Routes  
✅ JWT middleware  
✅ Validation  
✅ Error handling  
✅ Database connection  
✅ package.json  

### .NET Backend (C#)
✅ Entity models  
✅ DTOs  
✅ Controllers  
✅ Services  
✅ DbContext  
✅ JWT authentication  
✅ Middleware  
✅ .csproj file  

### JavaScript/TypeScript Frontend
✅ Type-safe API client  
✅ Model classes  
✅ Service layer  
✅ Authentication manager  
✅ Error handling  
✅ Request/response interceptors  

### Flutter Frontend (Dart)
✅ Dart models with JSON serialization  
✅ API services  
✅ HTTP client with Dio  
✅ Authentication management  
✅ Error handling  
✅ pubspec.yaml  

### Swift Frontend (iOS)
✅ Codable models  
✅ API services  
✅ URLSession networking  
✅ KeyChain authentication  
✅ Error handling  
✅ Swift Package  

## Examples

### E-commerce API

```yaml
project:
  name: ShopAPI
  version: 1.0.0
  base_url: https://api.myshop.com

models:
  Product:
    fields:
      id: integer
      name: string
      description: text
      price: float
      stock: integer
      category_id: integer
    timestamps: true
    
  Order:
    fields:
      id: integer
      user_id: integer
      total: float
      status: string
    timestamps: true
    
  OrderItem:
    fields:
      id: integer
      order_id: integer
      product_id: integer
      quantity: integer
      price: float

endpoints:
  - resource: products
    model: Product
    operations: [create, read, update, delete, list, search]
    auth_required: false
    pagination: true
    filters: [category_id]
    
  - resource: orders
    model: Order
    operations: [create, read, list]
    auth_required: true
```

### Social Media API

```yaml
project:
  name: SocialAPI
  version: 1.0.0
  base_url: https://api.mysocial.com

models:
  User:
    fields:
      id: integer
      username: string
      email: string
      bio: text
      avatar_url: string
    timestamps: true
    
  Post:
    fields:
      id: integer
      user_id: integer
      content: text
      image_url: string
      likes_count: integer
    timestamps: true
    
  Comment:
    fields:
      id: integer
      post_id: integer
      user_id: integer
      content: text
    timestamps: true

endpoints:
  - resource: users
    model: User
    operations: [create, read, update, list]
    
  - resource: posts
    model: Post
    operations: [create, read, update, delete, list]
    filters: [user_id]
    sort_fields: [created_at, likes_count]
    
  - resource: comments
    model: Comment
    operations: [create, read, delete, list]
    filters: [post_id, user_id]
```

## Configuration Tips

### Field Validation

```yaml
models:
  User:
    fields:
      username:
        type: string
        required: true
        min_length: 3
        max_length: 30
        unique: true
      email:
        type: string
        required: true
        pattern: "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        unique: true
      age:
        type: integer
        min_value: 13
        max_value: 120
```

### Foreign Keys

```yaml
models:
  Post:
    fields:
      user_id:
        type: integer
        required: true
        foreign_key: User  # References User model
```

### Authentication Types

```yaml
auth:
  type: jwt  # JWT tokens (default)
  # type: oauth2  # OAuth2
  # type: api_key  # API key
  # type: none  # No authentication
```

### Database Options

```yaml
database:
  type: postgresql  # postgresql, mysql, sqlite, mongodb
  migrations: true  # Generate migration files
```

## Advanced Features

### Custom Endpoints

```yaml
endpoints:
  - resource: users
    model: User
    operations: [create, read, update, delete, list]
    custom_endpoints:
      - name: activate
        method: POST
        path: /users/{id}/activate
      - name: deactivate
        method: POST
        path: /users/{id}/deactivate
```

### Pagination Configuration

```yaml
endpoints:
  - resource: posts
    model: Post
    pagination: true
    page_size: 20        # Default page size
    max_page_size: 100   # Maximum allowed
```

### Filtering & Sorting

```yaml
endpoints:
  - resource: posts
    model: Post
    filters: [user_id, published, category]
    sort_fields: [created_at, title, views]
```

Then query like:
```
GET /api/posts?user_id=5&published=true&sort_by=created_at&order=desc&page=1&page_size=20
```

## Troubleshooting

### Configuration Errors
```bash
adipose validate --config your-config.yaml
```

### Generated Code Issues
1. Check that all models are defined
2. Verify foreign key references exist
3. Ensure operations list is valid

### Can't Find Executable
```bash
# Make it executable
chmod +x adipose

# Add to PATH (Linux/Mac)
export PATH=$PATH:/path/to/adipose
```

## Next Steps

1. **Read Full Docs**: See `DOCUMENTATION.md` for complete reference
2. **Customize Generated Code**: Add your business logic to generated files
3. **Deploy**: Generated code is production-ready!
4. **Contribute**: Add your own backend/frontend generators

## Support

- **Documentation**: See DOCUMENTATION.md
- **Issues**: https://github.com/yourusername/adipose/issues
- **Discussions**: https://github.com/yourusername/adipose/discussions

## License

MIT License - Free for personal and commercial use!

---

**Made with ❤️ by the Adipose team**

*Generate less. Build more.*
