# Building Standalone Executables

This guide explains how to build standalone executables for Linux, macOS, and Windows. The executables are completely self-contained and require no Python installation or external dependencies.

## Quick Build (Linux/Mac)

```bash
./build.sh
```

This will create:
- `dist/adipose` - Standalone executable
- `dist/adipose-[Platform]-[Arch]-v0.1.0.tar.gz` - Distribution package

## Platform-Specific Instructions

### Linux

#### Prerequisites
- Python 3.8 or higher
- Git (optional)

#### Build Steps

```bash
# 1. Clone repository (if needed)
git clone https://github.com/yourusername/adipose.git
cd adipose

# 2. Run build script
./build.sh

# 3. Test executable
./dist/adipose --version
./dist/adipose list-platforms
```

#### Distribution Package Contents
```
adipose-Linux-x86_64-v0.1.0/
├── adipose                 # Standalone executable (14MB)
├── README.md              # Project README
├── DOCUMENTATION.md       # Full documentation
├── example-config.yaml    # Example configuration
└── INSTALL.txt           # Installation instructions
```

#### Manual Build (if build.sh fails)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build
pyinstaller adipose.spec --clean

# Test
./dist/adipose --version
```

---

### macOS

#### Prerequisites
- Python 3.8 or higher (install via Homebrew: `brew install python3`)
- Xcode Command Line Tools: `xcode-select --install`

#### Build Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/adipose.git
cd adipose

# 2. Make build script executable
chmod +x build.sh

# 3. Run build
./build.sh
```

This creates: `adipose-Darwin-x86_64-v0.1.0.tar.gz` (or arm64 for M1/M2 Macs)

#### Signing for macOS (Optional)

To avoid "unidentified developer" warnings:

```bash
# Sign the executable
codesign --force --deep --sign - dist/adipose

# Or for distribution
codesign --force --deep --sign "Developer ID Application: Your Name" dist/adipose
```

#### Creating Universal Binary (Intel + Apple Silicon)

```bash
# Build on Intel Mac
./build.sh
mv dist/adipose dist/adipose-x86_64

# Build on Apple Silicon Mac  
./build.sh
mv dist/adipose dist/adipose-arm64

# Create universal binary
lipo -create -output dist/adipose dist/adipose-x86_64 dist/adipose-arm64
```

---

### Windows

#### Prerequisites
- Python 3.8 or higher (download from python.org)
- Git for Windows (optional)

#### Build Steps (PowerShell)

```powershell
# 1. Clone repository
git clone https://github.com/yourusername/adipose.git
cd adipose

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 4. Build
pyinstaller adipose.spec --clean

# 5. Test
.\dist\adipose.exe --version
```

#### Build Steps (Command Prompt)

```cmd
REM 1. Clone repository
git clone https://github.com/yourusername/adipose.git
cd adipose

REM 2. Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

REM 3. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

REM 4. Build
pyinstaller adipose.spec --clean

REM 5. Test
dist\adipose.exe --version
```

#### Creating Windows Installer (Optional)

Using NSIS (Nullsoft Scriptable Install System):

```nsis
; adipose-installer.nsi
!define APP_NAME "Adipose"
!define VERSION "0.1.0"

Name "${APP_NAME} ${VERSION}"
OutFile "adipose-setup-v${VERSION}.exe"
InstallDir "$PROGRAMFILES\Adipose"

Section
    SetOutPath $INSTDIR
    File "dist\adipose.exe"
    File "README.md"
    File "DOCUMENTATION.md"
    
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Add to PATH
    EnVar::AddValue "PATH" "$INSTDIR"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\adipose.exe"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
SectionEnd
```

---

## Customizing the Build

### Reducing Executable Size

Edit `adipose.spec`:

```python
# Enable UPX compression
upx=True,
upx_exclude=[],

# Exclude unnecessary modules
excludes=['tkinter', 'matplotlib', 'numpy', 'pandas'],

# Strip debug symbols
strip=True,
```

### Adding Icon (Windows/Mac)

```python
# In adipose.spec, EXE section:
icon='path/to/icon.ico',  # Windows
icon='path/to/icon.icns', # macOS
```

### Debug Build

```python
# In adipose.spec:
debug=True,
console=True,  # Always True for CLI apps
```

---

## CI/CD Automated Builds

### GitHub Actions

Create `.github/workflows/build.yml`:

```yaml
name: Build Executables

on:
  push:
    tags:
      - 'v*'

jobs:
  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Build
        run: ./build.sh
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: adipose-linux
          path: dist/*.tar.gz

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Build
        run: ./build.sh
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: adipose-macos
          path: dist/*.tar.gz

  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Build
        run: |
          python -m venv venv
          .\venv\Scripts\Activate.ps1
          pip install -r requirements.txt
          pip install pyinstaller
          pyinstaller adipose.spec --clean
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: adipose-windows
          path: dist/adipose.exe
```

---

## Testing the Executable

### Basic Tests

```bash
# Version check
./dist/adipose --version

# List platforms
./dist/adipose list-platforms

# Create example config
./dist/adipose init --output test.yaml

# Validate config
./dist/adipose validate --config test.yaml

# Generate code
./dist/adipose generate --config test.yaml --backend django --output ./out
```

### Comprehensive Test

```bash
# Create test directory
mkdir adipose-test && cd adipose-test

# Initialize config
../dist/adipose init --output api.yaml

# Validate
../dist/adipose validate --config api.yaml

# Generate Django backend
../dist/adipose generate --config api.yaml --backend django --output ./backend

# Verify generated files
ls -R backend/

# Test generated code
cd backend
pip install -r requirements.txt
python manage.py check
```

---

## Distribution

### File Sizes (Approximate)

- **Linux (x86_64)**: ~14MB
- **macOS (Intel)**: ~15MB
- **macOS (ARM64)**: ~14MB
- **Windows**: ~16MB

### Checksums

Generate checksums for distribution:

```bash
# Linux/Mac
sha256sum dist/adipose-*.tar.gz > checksums.txt
md5sum dist/adipose-*.tar.gz >> checksums.txt

# Windows (PowerShell)
Get-FileHash dist\adipose.exe -Algorithm SHA256 > checksums.txt
Get-FileHash dist\adipose.exe -Algorithm MD5 >> checksums.txt
```

### GitHub Release

```bash
# Create release with all platform builds
gh release create v0.1.0 \
  dist/adipose-Linux-x86_64-v0.1.0.tar.gz \
  dist/adipose-Darwin-x86_64-v0.1.0.tar.gz \
  dist/adipose-Darwin-arm64-v0.1.0.tar.gz \
  dist/adipose-Windows-x86_64-v0.1.0.zip \
  --title "Adipose v0.1.0" \
  --notes "Standalone executables for all platforms"
```

---

## Troubleshooting

### "Permission denied" on Linux/Mac
```bash
chmod +x dist/adipose
```

### "Cannot be opened because it is from an unidentified developer" (macOS)
```bash
# Option 1: Right-click -> Open
# Option 2: Remove quarantine attribute
xattr -dr com.apple.quarantine dist/adipose
```

### Missing DLL errors (Windows)
- Install Visual C++ Redistributable
- Rebuild with `--onefile` flag

### Large executable size
- Enable UPX compression in spec file
- Exclude unnecessary modules
- Use `--strip` option

### Module not found errors
- Add missing modules to `hiddenimports` in adipose.spec
- Check PyInstaller hooks

---

## Support

For build issues:
1. Check PyInstaller documentation: https://pyinstaller.org
2. Open GitHub issue with build logs
3. Include platform and Python version

---

## License

Built executables retain the same MIT license as the source code.
