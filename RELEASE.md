# 🚀 Release Process

This document outlines the automated release process for baseline-cli using GitHub Actions and helper scripts.

## Quick Release Guide

### 1. Update the Changelog

First, update `CHANGELOG.md` with the new version entry following the [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [0.1.3] - 2024-12-31

### Added
- New feature descriptions here

### Changed  
- Changes to existing functionality

### Fixed
- Bug fixes and corrections
```

### 2. Use the Release Helper Script

The release helper script automates version bumping, git tagging, and release creation:

```bash
# Preview the release (dry run)
python scripts/release.py 0.1.3 --dry-run

# Create the actual release
python scripts/release.py 0.1.3
```

### 3. Monitor the Release

Once the tag is pushed, the GitHub Actions workflow will:
- ✅ Run all tests to ensure quality
- ✅ Verify version consistency between tag and `__version__.py`
- ✅ Extract changelog content for the release notes
- ✅ Create a GitHub Release with proper formatting
- ✅ Upload release assets (requirements.txt)

## Manual Release Process

If you prefer to create releases manually:

### 1. Update Version

Edit `__version__.py`:
```python
__version__ = "0.1.3"  # Update this line
```

### 2. Commit and Tag

```bash
# Commit the version change
git add __version__.py
git commit -m "Bump version to 0.1.3"

# Create and push the tag
git tag -a v0.1.3 -m "Release v0.1.3"
git push origin v0.1.3
```

### 3. GitHub Actions Takes Over

The release workflow automatically triggers and handles the rest.

## Release Workflow Details

### Trigger
```yaml
on:
  push:
    tags:
      - 'v*'  # Any tag starting with 'v' (e.g., v0.1.3, v1.0.0)
```

### Process
1. **Checkout & Setup**: Retrieves code and sets up Python environment
2. **Quality Gate**: Runs full test suite - release fails if tests fail
3. **Version Validation**: Ensures tag version matches `__version__.py`
4. **Changelog Extraction**: Automatically extracts release notes from `CHANGELOG.md`
5. **Release Creation**: Creates GitHub Release with extracted changelog
6. **Asset Upload**: Attaches relevant files to the release

### Pre-release Detection
The workflow automatically marks releases as pre-release if the version contains:
- Hyphens (e.g., `v1.0.0-beta`)
- `alpha`, `beta`, or `rc` keywords

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible
- **Pre-release** (0.0.X-beta): Development versions

### Examples
```bash
# Patch release (bug fixes)
python scripts/release.py 0.1.3

# Minor release (new features)  
python scripts/release.py 0.2.0

# Major release (breaking changes)
python scripts/release.py 1.0.0

# Pre-release versions
python scripts/release.py 0.2.0-beta
python scripts/release.py 1.0.0-rc.1
```

## Troubleshooting

### Release Helper Script Issues

**Problem**: `❌ Working directory has uncommitted changes`
```bash
# Solution: Commit or stash your changes
git add .
git commit -m "Your commit message"
# OR
git stash
```

**Problem**: `⚠️ No changelog entry found for version X.X.X`
```bash
# Solution: Add the version section to CHANGELOG.md
## [X.X.X] - YYYY-MM-DD
### Added
- Your changes here
```

**Problem**: `❌ Version mismatch! Tag version: X.X.X Package version: Y.Y.Y`
```bash
# Solution: The script should handle this automatically, but if it fails:
# Manually update __version__.py to match your intended release version
```

### GitHub Actions Issues

**Problem**: Release workflow fails on tests
```bash
# Solution: Fix the failing tests before creating the release
pytest  # Run tests locally first
```

**Problem**: Permission denied when creating release
```bash
# Solution: Ensure your repository has the correct permissions
# The workflow uses GITHUB_TOKEN which should work automatically
# If issues persist, check repository settings > Actions > General
```

**Problem**: Changelog extraction fails
```bash
# Solution: Ensure your CHANGELOG.md follows the expected format:
## [VERSION] - DATE
### Added
- Changes here
```

## Release Assets

Currently, the workflow uploads:
- `requirements.txt` - Python dependencies

### Adding More Assets

To add more files to releases, modify `.github/workflows/release.yml`:

```yaml
- name: Upload Additional Asset
  uses: actions/upload-release-asset@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    upload_url: ${{ steps.create_release.outputs.upload_url }}
    asset_path: ./path/to/your/file
    asset_name: filename-in-release
    asset_content_type: application/octet-stream
```

## Security Considerations

- The release workflow only triggers on version tags (`v*`)
- Uses repository's `GITHUB_TOKEN` for authentication
- Runs in isolated GitHub Actions environment
- All changes are version controlled and auditable

## Best Practices

1. **Always test before releasing**: The workflow runs tests, but test locally first
2. **Keep changelog updated**: Helps users understand what changed
3. **Use semantic versioning**: Makes it clear what type of changes are included
4. **Review the dry run**: Always use `--dry-run` first to preview changes
5. **Monitor the workflow**: Check GitHub Actions tab to ensure release completes successfully

## Examples

### Typical Release Flow

```bash
# 1. Make changes and commit them
git add .
git commit -m "Add new feature"

# 2. Update CHANGELOG.md with new version section
# [Add your changes to CHANGELOG.md]

# 3. Test the release process
python scripts/release.py 0.1.3 --dry-run

# 4. Create the actual release
python scripts/release.py 0.1.3

# 5. Monitor at: https://github.com/your-username/baseline-cli/actions
```

### Hotfix Release

```bash
# For urgent bug fixes, you can skip the minor version
# Current: 0.1.2 → Hotfix: 0.1.3
python scripts/release.py 0.1.3
```

### Feature Release

```bash
# For new features, bump the minor version
# Current: 0.1.2 → Feature: 0.2.0
python scripts/release.py 0.2.0
```

---

💡 **Need help?** Check the [GitHub Actions workflow logs](https://github.com/your-username/baseline-cli/actions) for detailed information about any release issues. 