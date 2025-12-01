# Adipose v0.1.0

**Generate production-ready backend and frontend API layers from a single config file!**

No Python required - this is a standalone executable.

## What's Included

```
adipose-[Platform]-[Arch]-v0.1.0/
├── adipose (or adipose.exe on Windows)  # Standalone executable (~14MB)
├── README.md                             # This file
├── DOCUMENTATION.md                      # Complete reference guide
├── example-config.yaml                   # Sample API configuration
└── INSTALL.txt                          # Installation instructions
```

## Quick Start (3 Steps)

### 1. Make Executable (Linux/Mac only)
```bash
chmod +x adipose
```

### 2. Create Your API Config
```bash
./adipose init --output my-api.yaml
# Edit my-api.yaml with your models and endpoints
```

### 3. Generate Code
```bash
# Django backend
./adipose generate --config my-api.yaml --backend django --output ./backend

# Swift iOS frontend
./adipose generate --config my-api.yaml --frontend swift --output ./ios-app

# Or both!
./adipose generate --config my-api.yaml --backend express --frontend flutter --output ./app
```

## Available Commands

```bash
./adipose --help              # Show all commands
./adipose --version           # Show version
./adipose list-platforms      # List all supported frameworks
./adipose init               # Create example configuration
./adipose validate -c file.yaml   # Validate configuration
./adipose generate -c file.yaml -b django -o ./out   # Generate code
```

## Supported Platforms

### Backend Frameworks (5)
- **django** - Django REST Framework (Python)
- **express** - Express.js with TypeScript (Node.js)
- **dotnet** - ASP.NET Core (C#)
- **springboot** - Spring Boot (Java)
- **laravel** - Laravel API (PHP)

### Frontend Frameworks (5)
- **javascript** / **typescript** - Axios-based API client
- **flutter** - Flutter/Dart mobile app
- **swift** - iOS native (Swift)
- **kotlin** - Android native (Kotlin)
- **avaloniaui** - Cross-platform desktop (C#)

## Example Configuration

See `example-config.yaml` for a complete blog API example, or create your own:

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
    timestamps: true

endpoints:
  - resource: users
    model: User
    operations: [create, read, update, delete, list]
    auth_required: true
```

## What Gets Generated

### Django Backend Example
- ✅ Models with field validation
- ✅ Serializers with custom validation
- ✅ ViewSets with CRUD operations
- ✅ JWT authentication middleware
- ✅ URL routing configuration
- ✅ CORS settings
- ✅ Error handling
- ✅ Pagination, filtering, sorting
- ✅ Database configuration
- ✅ requirements.txt

**Ready to run:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Your API is live at http://localhost:8000/api/
```

## Installation to PATH (Optional)

To use `adipose` from anywhere:

**Linux:**
```bash
sudo cp adipose /usr/local/bin/
adipose --version
```

**Mac:**
```bash
sudo cp adipose /usr/local/bin/
adipose --version
```

**Windows (PowerShell as Admin):**
```powershell
Move-Item adipose.exe C:\Windows\System32\
adipose --version
```

## Configuration Features

- 📝 Multiple models with relationships
- 🔗 Foreign keys between models
- ✅ Field validation (min/max, patterns, unique)
- 🔐 JWT/OAuth2/API Key authentication
- 📄 Pagination with configurable sizes
- 🔍 Filtering and sorting
- 🌐 CORS configuration
- 🗄️ Multiple databases (PostgreSQL, MySQL, SQLite, MongoDB)
- 🚨 Error handling
- 📊 Custom endpoints beyond CRUD

## Complete Workflow Example

```bash
# 1. Create new API project
./adipose init --output blog-api.yaml

# 2. Edit the configuration (add your models and endpoints)
# ... edit blog-api.yaml ...

# 3. Validate before generating
./adipose validate --config blog-api.yaml

# 4. Generate Django backend
./adipose generate --config blog-api.yaml --backend django --output ./my-blog-backend

# 5. Generate Flutter mobile app
./adipose generate --config blog-api.yaml --frontend flutter --output ./my-blog-app

# 6. Run the backend
cd my-blog-backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# 7. Your API is ready!
# Backend: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

## System Requirements

- **Linux**: Any modern distribution (glibc 2.27+)
- **macOS**: macOS 10.13 or later
- **Windows**: Windows 10 or later

**No additional software required!** This executable includes:
- Python runtime
- All dependencies
- Template files
- Everything needed to generate code

## File Size

- Executable: ~14MB (uncompressed)
- Archive: ~5MB (compressed)

## Documentation

- **DOCUMENTATION.md** - Complete reference guide (350+ lines)
- **Configuration** - All field types, validation options, examples
- **Generated Code** - What each framework produces
- **Advanced Features** - Custom endpoints, filtering, sorting

## Troubleshooting

### "Permission denied" (Linux/Mac)
```bash
chmod +x adipose
```

### "Cannot be opened because it is from an unidentified developer" (macOS)
```bash
xattr -dr com.apple.quarantine adipose
# Or: Right-click -> Open
```

### Generated code has errors
1. Validate your config first: `./adipose validate --config your-config.yaml`
2. Check that all models are defined
3. Verify foreign key references exist
4. Ensure operations list is valid

### Need help?
- Read DOCUMENTATION.md for complete reference
- Check example-config.yaml for working examples
- Visit: https://github.com/yourusername/adipose/issues

## Features Highlights

### 🚀 Fast
- Code generation: <1 second
- Startup time: <100ms
- No compilation needed

### 🎯 Production-Ready
- Industry-standard libraries
- Framework best practices
- Complete error handling
- Security built-in

### 💡 Easy to Use
- Simple YAML configuration
- Validate before generating
- Comprehensive examples
- Detailed documentation

### 🔧 Extensible
- Multiple backends
- Multiple frontends
- Mix and match freely

## Example: E-commerce API

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

endpoints:
  - resource: products
    model: Product
    operations: [create, read, update, delete, list, search]
    pagination: true
    filters: [category_id]
    
  - resource: orders
    model: Order
    operations: [create, read, list]
    auth_required: true
```

Generate all this with one command:
```bash
./adipose generate --config shop-api.yaml --backend django --output ./shop-backend
```

## What You Get

For a typical API with 3 models:
- **Configuration:** ~60 lines of YAML
- **Generated Code:** ~1000+ lines of production-ready code
- **Time Saved:** Hours or days of boilerplate coding

## License

MIT License - Free for personal and commercial use!

## Version

Adipose v0.1.0 (December 2025)

---

**Get Started Now:**
```bash
./adipose init --output my-api.yaml
./adipose generate --config my-api.yaml --backend django --output ./backend
```

*Generate less. Build more.* 🚀
