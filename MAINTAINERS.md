# Documentation for Maintainers

Since this is a Python tool used for game automation across multiple platforms, it's important to document the maintenance procedures.

## Building Releases

### Prerequisites

- Python 3.8+ installed on each target platform
- Git access to the repository
- GitHub release permissions

### Release Checklist

- [ ] All tests pass on CI
- [ ] Linux executable built and uploaded (automated)
- [ ] macOS executable built and uploaded (automated)
- [ ] Windows executable built and uploaded (automated)
- [ ] Release notes updated
- [ ] Download links verified
- [ ] Installation instructions updated in README

### Making a Release

#### 1. Prepare Release
- [ ] Write changelog entries
- [ ] Update version references if needed
- [ ] Test on all platforms
- [ ] Commit all changes

#### 2. Create Release Tag
```bash
# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

#### 3. Automated Builds (All Platforms)
- GitHub Actions will automatically build Linux, macOS, and Windows executables
- ViGEmBus driver is automatically installed during Windows builds
- Artifacts are uploaded to the release

#### 4. (optional) Manual Build (Fallback Only)
If CI Windows build fails, build manually:

```bash
# On Windows machine with ViGEmBus installed:

# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Build executable
python build.py

# 4. Create versioned copies
copy dist\pano-capture.exe dist\pano-capture-[VERSION]-windows.exe
```

#### 5. (optional) Upload Build to Release
- Go to the [GitHub release page](https://github.com/Respawwwn/game-pano-capture/releases)
- Edit the release created by the tag
- Upload the Windows executables:
  - `pano-capture-[VERSION]-windows.exe`

#### 6. (optional) Update Release Notes
Update the GitHub release with:
- **Changelog** entries
- **Download instructions** for all platforms
- **Known issues** if any

#### 7. (optional) Upload and replace the "latest" build
Update the GitHub "latest" release with:
- `pano-capture-latest-windows.exe`
- `pano-capture-latest-macos.exe`
- `pano-capture-latest-linux.exe`

### Testing Releases

Before finalizing, test each platform executable:

```bash
# Test help output
./pano-capture --help

# Test setup (should show configuration prompts)
./pano-capture --setup "Test Game"

# Test that modules load correctly
./pano-capture --list
```

### Troubleshooting

#### Windows Build Issues
- **ViGEmBus not found**: Install ViGEmBus driver from official releases
- **Compilation errors**: Install Visual Studio Build Tools
- **Missing dependencies**: Ensure all requirements.txt packages install successfully

### Version Naming Convention

- **Tags**: `v1.0.0`, `v1.1.0`, `v2.0.0` (with v prefix)
- **Executables**: 
  - Versioned: `pano-capture-1.0.0-{platform}.exe` (no v prefix)
