#!/bin/bash
# Build script for Adipose standalone executables

set -e

echo "==========================================="
echo "Adipose Standalone Executable Builder"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect platform
PLATFORM=$(uname -s)
echo -e "${BLUE}Detected platform: ${PLATFORM}${NC}"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -q -r requirements.txt
pip install -q pyinstaller

# Clean previous builds
echo -e "${BLUE}Cleaning previous builds...${NC}"
rm -rf build dist
mkdir -p dist

# Build executable
echo -e "${BLUE}Building standalone executable...${NC}"
pyinstaller adipose.spec --clean

# Test the executable
echo ""
echo -e "${BLUE}Testing executable...${NC}"
./dist/adipose --version
echo ""

# Get file size
SIZE=$(du -h dist/adipose | cut -f1)

# Display success message
echo ""
echo -e "${GREEN}✓ Build successful!${NC}"
echo ""
echo "Executable location: ./dist/adipose"
echo "File size: ${SIZE}"
echo ""
echo "Test commands:"
echo "  ./dist/adipose --help"
echo "  ./dist/adipose list-platforms"
echo "  ./dist/adipose init --output test-api.yaml"
echo ""

# Create distribution package
echo -e "${BLUE}Creating distribution package...${NC}"
DIST_NAME="adipose-${PLATFORM}-$(uname -m)-v0.1.0"
mkdir -p "dist/${DIST_NAME}"
cp dist/adipose "dist/${DIST_NAME}/"
cp README.md "dist/${DIST_NAME}/"
cp DOCUMENTATION.md "dist/${DIST_NAME}/"
cp examples/blog-api.yaml "dist/${DIST_NAME}/example-config.yaml"

# Create installation instructions
cat > "dist/${DIST_NAME}/INSTALL.txt" << 'EOF'
ADIPOSE - Installation Instructions
====================================

1. Extract this archive to any directory
2. Add the executable to your PATH (optional):
   
   Linux/Mac:
   sudo cp adipose /usr/local/bin/
   
   Or add to your shell profile:
   export PATH=$PATH:/path/to/adipose
   
3. Run adipose:
   ./adipose --help
   ./adipose list-platforms
   ./adipose init --output my-api.yaml

4. Generate code:
   ./adipose generate --config my-api.yaml --backend django --output ./backend

For full documentation, see DOCUMENTATION.md

No Python installation required - this is a standalone executable!
EOF

# Create tarball
cd dist
tar -czf "${DIST_NAME}.tar.gz" "${DIST_NAME}"
cd ..

echo ""
echo -e "${GREEN}✓ Distribution package created!${NC}"
echo ""
echo "Package: dist/${DIST_NAME}.tar.gz"
echo ""
echo "To distribute:"
echo "  1. Upload dist/${DIST_NAME}.tar.gz to GitHub releases"
echo "  2. Users can extract and run without Python"
echo ""
