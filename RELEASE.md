# 🚀 Release Process

This document outlines the **fully automated** release process for baseline-cli using GitHub Actions.

## 🎯 **Automated Release Workflow**

Releases are **automatically created** when you merge changes to the `main` branch that include a version bump in `__version__.py`. No manual tagging required!

### How It Works
1. **Update version** in `__version__.py` 
2. **Update CHANGELOG.md** with new version entry
3. **Merge to main** → GitHub Actions automatically creates the release!

## Quick Release Guide

### 1. Update the Changelog

Update `CHANGELOG.md` with the new version entry:

```markdown
## [0.2.0] - 2024-12-31

### Added
- New feature descriptions here

### Changed  
- Changes to existing functionality

### Fixed
- Bug fixes and corrections
```

### 2. Use the Release Helper Script (Recommended)

The release helper script prepares everything for the automated workflow:

```bash
# Preview the release preparation (dry run)
python3 scripts/release.py 0.2.0 --dry-run

# Prepare the release (recommended approach)
python3 scripts/release.py 0.2.0 --commit-only
```

### 3. Push/Merge to Main

Once you push or merge the version change to `main`:
- ✅ GitHub Actions automatically detects the version change
- ✅ Runs full test suite to ensure quality
- ✅ Creates git tag (`v0.2.0`)
- ✅ Extracts changelog content for release notes
- ✅ Creates GitHub Release with proper formatting
- ✅ Uploads release assets

## Manual Release Preparation

If you prefer to handle version bumping manually:

### 1. Update Version

Edit `__version__.py`:
```python
__version__ = "0.2.0"  # Update this line
```

### 2. Update Changelog

Add your version section to `CHANGELOG.md`

### 3. Commit and Push

```bash
git add __version__.py CHANGELOG.md
git commit -m "Bump version to 0.2.0"
git push origin your-branch
```

### 4. Merge to Main

Create a PR and merge to `main` → **GitHub Actions automatically creates the release!**

## Release Workflow Details

### Automatic Triggers
```yaml
on:
  push:
    branches: [main]
    paths: ['__version__.py']  # Only triggers when version file changes
```

### Manual Triggers (Still Supported)
```yaml
on:
  push:
    tags: ['v*']  # Manual tag pushes still work
```

### Workflow Process
1. **Version Detection**: Reads current version from `__version__.py`
2. **Duplicate Check**: Prevents creating duplicate releases
3. **Quality Gate**: Runs full test suite - release fails if tests fail
4. **Changelog Extraction**: Automatically extracts release notes from `CHANGELOG.md`
5. **Tag Creation**: Creates git tag automatically (`v{version}`)
6. **Release Creation**: Creates GitHub Release with extracted changelog
7. **Asset Upload**: Attaches relevant files to the release

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
python3 scripts/release.py 0.2.1 --commit-only

# Minor release (new features)  
python3 scripts/release.py 0.3.0 --commit-only

# Major release (breaking changes)
python3 scripts/release.py 1.0.0 --commit-only

# Pre-release versions
python3 scripts/release.py 0.3.0-beta --commit-only
python3 scripts/release.py 1.0.0-rc.1 --commit-only
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

### GitHub Actions Issues

**Problem**: Release workflow doesn't trigger after merge
```bash
# Check: Did you update __version__.py in your merge?
# The workflow only triggers when __version__.py changes on main
```

**Problem**: Release workflow fails on tests
```bash
# Solution: Fix the failing tests before merging
pytest  # Run tests locally first
```

**Problem**: "Release already exists" message
```bash
# This is normal - the workflow prevents duplicate releases
# Check if the release actually exists on GitHub
```

**Problem**: Changelog extraction fails
```bash
# Solution: Ensure your CHANGELOG.md follows the expected format:
## [VERSION] - DATE
### Added
- Changes here
```

## Comparison: Old vs New Workflow

### ❌ **Old Manual Process**
```bash
# Multiple steps, error-prone
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
# Wait for GitHub Actions
# Manual release creation if it fails
```

### ✅ **New Automated Process** 
```bash
# Single step
python3 scripts/release.py 0.2.0 --commit-only
git push origin main  # (or merge PR)
# Everything else happens automatically!
```

## Release Assets

Currently, the workflow uploads:
- `requirements.txt` - Python dependencies

### Adding More Assets

To add more files to releases, modify `.github/workflows/release.yml`:

```yaml
- name: Upload Additional Asset
  if: steps.check_release.outputs.exists == 'false'
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

- Workflow only triggers on `main` branch version changes
- Uses repository's `GITHUB_TOKEN` for authentication
- Runs in isolated GitHub Actions environment
- All changes are version controlled and auditable
- Prevents duplicate releases automatically

## Best Practices

1. **Use the release helper script**: Reduces errors and ensures consistency
2. **Always test before merging**: The workflow runs tests, but test locally first
3. **Keep changelog updated**: Required for proper release notes
4. **Use semantic versioning**: Makes it clear what type of changes are included
5. **Review PRs carefully**: Once merged to main, the release is automatic
6. **Monitor workflows**: Check GitHub Actions tab to ensure release completes successfully

## Examples

### Typical Release Flow (Recommended)

```bash
# 1. Make changes and commit them on feature branch
git checkout -b feature/new-feature
# ... make changes ...
git add .
git commit -m "Add new feature"

# 2. Update CHANGELOG.md and version
# [Add your changes to CHANGELOG.md]
python3 scripts/release.py 0.2.0 --commit-only

# 3. Push and create PR
git push origin feature/new-feature
# Create PR on GitHub

# 4. Merge PR to main
# → GitHub Actions automatically creates release v0.2.0! 🎉
```

### Hotfix Release

```bash
# For urgent bug fixes from main branch
git checkout main
git pull origin main
# ... fix the bug ...
python3 scripts/release.py 0.2.1 --commit-only  # Patch version
git push origin main  # → Automatic release!
```

### Feature Release

```bash
# For new features (development branch → main)
python3 scripts/release.py 0.3.0 --commit-only  # Minor version
# Merge to main → Automatic release!
```

---

💡 **Need help?** Check the [GitHub Actions workflow logs](https://github.com/your-username/baseline-cli/actions) for detailed information about any release issues. 