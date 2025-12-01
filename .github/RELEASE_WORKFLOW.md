# GitHub Actions Release Guide

This guide explains how to use the automated build system to create releases with standalone executables for Linux, macOS, and Windows.

## Overview

The GitHub Actions workflow (`.github/workflows/build-release.yml`) automatically:
1. Builds standalone executables for Linux, macOS (Intel + ARM), and Windows
2. Tests each executable
3. Creates distribution packages with documentation
4. Generates checksums for security verification
5. Creates a GitHub release with all artifacts
6. Makes executables available for direct download

## Triggering a Release

### Method 1: Version Tag (Recommended)

Create and push a version tag to trigger an automatic release:

```bash
# Commit your changes
git add .
git commit -m "Release v0.1.0"

# Create a version tag
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push commits and tag
git push origin main
git push origin v0.1.0
```

The workflow will automatically:
- Build executables for all platforms
- Run tests on each platform
- Create a GitHub release
- Upload all distribution packages

### Method 2: Manual Trigger

You can also manually trigger the workflow from GitHub:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Build and Release Executables** workflow
4. Click **Run workflow** button
5. Select the branch and click **Run workflow**

**Note:** Manual triggers create artifacts but **not** GitHub releases (releases only happen with version tags).

## What Gets Built

### Linux (Ubuntu)
- **Platform:** x86_64
- **File:** `adipose-Linux-x86_64-v0.1.0.tar.gz`
- **Size:** ~14MB (compressed)
- **Compatibility:** glibc 2.27+ (Ubuntu 18.04+, CentOS 8+, Debian 10+)

### macOS Intel
- **Platform:** x86_64
- **File:** `adipose-Darwin-x86_64-v0.1.0.tar.gz`
- **Size:** ~15MB (compressed)
- **Compatibility:** macOS 10.13+ (High Sierra or later)

### macOS ARM (Apple Silicon)
- **Platform:** arm64 (M1/M2/M3)
- **File:** `adipose-Darwin-arm64-v0.1.0.tar.gz`
- **Size:** ~14MB (compressed)
- **Compatibility:** macOS 11+ (Big Sur or later)

### Windows
- **Platform:** x86_64
- **File:** `adipose-Windows-x86_64-v0.1.0.zip`
- **Size:** ~16MB (compressed)
- **Compatibility:** Windows 10 or later

## Build Process

Each platform build:

1. **Checks out code** from the repository
2. **Sets up Python 3.11** environment
3. **Installs dependencies** from requirements.txt
4. **Installs PyInstaller** for packaging
5. **Builds executable** using adipose.spec
6. **Tests the executable** (version check, list platforms)
7. **Creates distribution package** with:
   - Standalone executable
   - README.md (quick start guide)
   - DOCUMENTATION.md (complete reference)
   - example-config.yaml (sample configuration)
   - INSTALL.txt (installation instructions)
   - Checksums (SHA256 and MD5)
8. **Uploads artifacts** to GitHub

## Accessing Build Artifacts

### During Development (Before Release)

Access artifacts from the Actions tab:

1. Go to **Actions** tab
2. Click on the workflow run
3. Scroll down to **Artifacts** section
4. Download any platform's artifact

Artifacts are retained for **90 days**.

### In Releases (Production)

When you push a version tag, a GitHub Release is automatically created:

1. Go to **Releases** section (right sidebar or `/releases`)
2. Find your version (e.g., "Adipose v0.1.0")
3. Download the appropriate package for your platform
4. Verify checksums using SHA256SUMS.txt or MD5SUMS.txt

## Release Contents

Each release includes:

```
Release Assets:
├── adipose-Linux-x86_64-v0.1.0.tar.gz          # Linux package
├── adipose-Darwin-x86_64-v0.1.0.tar.gz         # macOS Intel package
├── adipose-Darwin-arm64-v0.1.0.tar.gz          # macOS ARM package
├── adipose-Windows-x86_64-v0.1.0.zip           # Windows package
├── SHA256SUMS.txt                               # SHA256 checksums
└── MD5SUMS.txt                                  # MD5 checksums
```

Each package contains:
- Standalone executable (no Python required)
- Complete documentation
- Example configuration
- Installation instructions

## Verification

Users can verify downloads using checksums:

```bash
# Linux/Mac
sha256sum -c SHA256SUMS.txt

# Or manually verify
sha256sum adipose-Linux-x86_64-v0.1.0.tar.gz
# Compare with SHA256SUMS.txt
```

```powershell
# Windows PowerShell
Get-FileHash adipose-Windows-x86_64-v0.1.0.zip -Algorithm SHA256
# Compare with SHA256SUMS.txt
```

## Workflow Customization

### Changing Version Number

Edit the version in multiple places:

1. **package-release.sh**: Update `VERSION="0.1.0"`
2. **setup.py**: Update `version="0.1.0"`
3. **pyproject.toml**: Update `version = "0.1.0"`
4. **Tag**: Use matching version tag (e.g., `v0.1.0`)

### Code Signing (Optional)

#### macOS Code Signing

To sign macOS executables (removes "unidentified developer" warning):

1. Add signing certificates to GitHub Secrets:
   - `MACOS_CERTIFICATE`
   - `MACOS_CERTIFICATE_PWD`
   - `MACOS_KEYCHAIN_PWD`

2. Enable signing in workflow:
   ```yaml
   - name: Sign executable
     if: true  # Change from false to true
     env:
       MACOS_CERTIFICATE: ${{ secrets.MACOS_CERTIFICATE }}
       MACOS_CERTIFICATE_PWD: ${{ secrets.MACOS_CERTIFICATE_PWD }}
     run: |
       # Import certificate
       echo $MACOS_CERTIFICATE | base64 --decode > certificate.p12
       security create-keychain -p "$MACOS_KEYCHAIN_PWD" build.keychain
       security import certificate.p12 -k build.keychain -P "$MACOS_CERTIFICATE_PWD"
       
       # Sign executable
       codesign --force --deep --sign "Developer ID Application: Your Name" dist/adipose
   ```

#### Windows Code Signing

To sign Windows executables:

1. Add code signing certificate to GitHub Secrets
2. Use `signtool.exe` in the workflow
3. Modify the Windows build job

### Building for Additional Platforms

To add support for other architectures:

```yaml
build-linux-arm64:
  name: Build Linux ARM64 Executable
  runs-on: ubuntu-latest
  steps:
    # Use cross-compilation or QEMU
    # Or use ARM-based runners if available
```

## Troubleshooting

### Build Fails on a Platform

1. Check the **Actions** tab for error logs
2. Common issues:
   - Missing dependencies in requirements.txt
   - Platform-specific import errors
   - PyInstaller compatibility issues

### Executable Doesn't Start

Test locally before releasing:

```bash
# Build locally
./build.sh

# Test
./dist/adipose --version
./dist/adipose list-platforms
```

### Release Not Created

Releases are only created when:
1. You push a **version tag** (e.g., `v0.1.0`)
2. The tag starts with `v`
3. All platform builds succeed

Check:
```bash
git tag  # List all tags
git push origin v0.1.0  # Make sure tag is pushed
```

### Artifacts Not Uploaded

Ensure artifact paths match in workflow:

```yaml
- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    path: dist/*.tar.gz  # Verify this path is correct
```

## Testing Releases

### Local Testing Before Release

```bash
# Build all platforms locally (if you have access to all platforms)
./build.sh
./package-release.sh

# Test executable
./dist/adipose --version
./dist/adipose init --output test.yaml
./dist/adipose validate --config test.yaml
./dist/adipose generate --config test.yaml --backend django --output ./test
```

### Pre-Release Testing

Create a pre-release tag:

```bash
git tag -a v0.1.0-beta.1 -m "Beta release"
git push origin v0.1.0-beta.1
```

Then mark the release as "pre-release" on GitHub.

## Release Checklist

Before creating a release:

- [ ] Update version numbers in all files
- [ ] Update CHANGELOG.md or release notes
- [ ] Test locally on your platform
- [ ] Commit all changes
- [ ] Create and push version tag
- [ ] Monitor GitHub Actions for build success
- [ ] Download and test artifacts from release
- [ ] Verify checksums
- [ ] Update documentation with new version
- [ ] Announce release

## Continuous Integration

The workflow also provides CI for pull requests (without creating releases):

```yaml
on:
  pull_request:
    branches: [ main ]
```

This will:
- Build executables for all platforms
- Run tests
- Upload artifacts (temporary)
- Not create a release

## Cost Considerations

GitHub Actions minutes:
- **Free tier:** 2,000 minutes/month for public repos
- **Each release build:** ~30-40 minutes total (all platforms)
- **Estimate:** ~50 releases/month on free tier

For private repos:
- **Free tier:** 500 minutes/month
- Consider using matrix builds strategically
- Cache dependencies to speed up builds

## Advanced: Matrix Builds

For faster parallel builds, use matrix strategy:

```yaml
jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-13, macos-14, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      # Build logic here
```

## Support

For issues with the build system:
1. Check GitHub Actions logs
2. Review this guide
3. Open an issue with:
   - Platform details
   - Build logs
   - Error messages

---

**Ready to release?**

```bash
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

Then watch the magic happen in the Actions tab! 🚀
