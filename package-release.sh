#!/bin/bash
# Package Adipose for distribution

set -e

echo "========================================"
echo "Adipose Release Packaging Script"
echo "========================================"
echo ""

# Detect platform
PLATFORM=$(uname -s)
ARCH=$(uname -m)
VERSION="0.1.0"
DIST_NAME="adipose-${PLATFORM}-${ARCH}-v${VERSION}"

echo "Creating distribution package: ${DIST_NAME}"
echo ""

# Create distribution directory
mkdir -p "dist/${DIST_NAME}"

# Copy executable
echo "✓ Copying executable..."
cp dist/adipose "dist/${DIST_NAME}/"

# Copy documentation
echo "✓ Copying documentation..."
cp RELEASE_README.md "dist/${DIST_NAME}/README.md"
cp DOCUMENTATION.md "dist/${DIST_NAME}/"

# Copy example config
echo "✓ Copying example configuration..."
cp examples/blog-api.yaml "dist/${DIST_NAME}/example-config.yaml"

# Create installation instructions
echo "✓ Creating installation instructions..."
cat > "dist/${DIST_NAME}/INSTALL.txt" << 'EOF'
ADIPOSE - Installation Instructions
====================================

Quick Start:
1. Extract this archive
2. Make executable: chmod +x adipose (Linux/Mac only)
3. Run: ./adipose --help

To install system-wide:
  Linux/Mac: sudo cp adipose /usr/local/bin/
  Windows: Move adipose.exe to C:\Windows\System32\

Usage:
  ./adipose init --output my-api.yaml
  ./adipose validate --config my-api.yaml
  ./adipose generate --config my-api.yaml --backend django --output ./backend

See README.md for complete documentation.

No Python installation required - this is a standalone executable!
EOF

# Make executable
chmod +x "dist/${DIST_NAME}/adipose"

# Create checksums (platform-specific)
echo "✓ Generating checksums..."
cd dist

# Detect which checksum commands are available
if command -v sha256sum &> /dev/null; then
    # Linux
    sha256sum "${DIST_NAME}/adipose" > "${DIST_NAME}/SHA256SUMS"
    md5sum "${DIST_NAME}/adipose" > "${DIST_NAME}/MD5SUMS"
elif command -v shasum &> /dev/null; then
    # macOS
    shasum -a 256 "${DIST_NAME}/adipose" > "${DIST_NAME}/SHA256SUMS"
    md5 -r "${DIST_NAME}/adipose" | awk '{print $1 "  " $2}' > "${DIST_NAME}/MD5SUMS"
else
    echo "Warning: No checksum utilities found, skipping checksums"
fi

# Create tarball
echo "✓ Creating archive..."
tar -czf "${DIST_NAME}.tar.gz" "${DIST_NAME}"

# Get sizes
EXEC_SIZE=$(du -h "${DIST_NAME}/adipose" | cut -f1)
ARCHIVE_SIZE=$(du -h "${DIST_NAME}.tar.gz" | cut -f1)

cd ..

echo ""
echo "========================================"
echo "✅ Release package created successfully!"
echo "========================================"
echo ""
echo "Package: dist/${DIST_NAME}.tar.gz"
echo "Executable size: ${EXEC_SIZE}"
echo "Archive size: ${ARCHIVE_SIZE}"
echo ""
echo "Contents:"
echo "  • adipose - Standalone executable"
echo "  • README.md - Quick start guide"
echo "  • DOCUMENTATION.md - Complete reference"
echo "  • example-config.yaml - Sample configuration"
echo "  • INSTALL.txt - Installation instructions"
echo "  • SHA256SUMS - Checksums for verification"
echo ""
echo "To test:"
echo "  cd dist/${DIST_NAME}"
echo "  ./adipose --version"
echo "  ./adipose list-platforms"
echo "  ./adipose init --output test.yaml"
echo ""
echo "To distribute:"
echo "  Upload dist/${DIST_NAME}.tar.gz to GitHub releases"
echo ""
