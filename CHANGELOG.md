# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2024-12-31

### Added
- **GitHub Releases Automation**: Complete automated release system with GitHub Actions workflow
- **Release Helper Script**: `scripts/release.py` for streamlined version bumping and release creation
- **Automated Changelog Extraction**: Release workflow automatically extracts changelog content for GitHub releases
- **Version Consistency Validation**: Ensures git tags match `__version__.py` before creating releases
- **Pre-release Detection**: Automatically identifies and marks beta/alpha/rc versions as pre-releases
- **Release Documentation**: Comprehensive `RELEASE.md` with step-by-step instructions and troubleshooting
- **Quality Gates**: Release workflow runs full test suite before creating releases
- **Release Assets**: Automatic upload of `requirements.txt` and other artifacts to releases

### Features
- **One-Command Releases**: `python3 scripts/release.py 0.2.0` handles entire release process
- **Dry Run Mode**: `--dry-run` flag for testing release process without making changes
- **Git Status Validation**: Prevents releases with uncommitted changes
- **Semantic Versioning Support**: Full support for major.minor.patch and pre-release versions
- **Beautiful Console Output**: Rich formatting for release helper script with progress indicators
- **Automated Git Tagging**: Creates and pushes version tags to trigger GitHub Actions workflow

### Technical Details
- **GitHub Actions Workflow**: `.github/workflows/release.yml` handles automated release creation
- **Tag-Based Triggers**: Releases trigger automatically on version tags (e.g., `v0.2.0`)
- **Changelog Integration**: Regex-based extraction of version-specific changelog content
- **Cross-Platform Compatibility**: Release helper works on macOS, Linux, and Windows
- **Error Handling**: Comprehensive error detection and user-friendly error messages
- **Security**: Uses repository's `GITHUB_TOKEN` for secure, scoped access

### Documentation
- **Release Process Guide**: Complete documentation in `RELEASE.md`
- **Troubleshooting Section**: Common issues and solutions for release workflow
- **Examples and Use Cases**: Step-by-step examples for different types of releases
- **Best Practices**: Guidelines for maintaining consistent release quality

## [0.1.2] - 2024-12-30

### Added
- New centralized error handling utilities in `utils/error_utils.py`
- Comprehensive test suite for error handling (`tests/test_error_utils.py`) with 26 dedicated tests
- `handle_cli_error()` function for standardized CLI error formatting with sys.exit()
- `handle_multiple_cli_errors()` function for displaying multiple error messages
- `format_function_error()` function for non-exit error scenarios
- `display_success_summary()` function for consistent success output formatting

### Changed
- **Consolidation**: Replaced duplicate error handling logic across all scripts
- **Consistency**: Standardized panel titles ("Baseline Capture Summary" vs "Baseline Comparison Summary")
- **Code Quality**: Reduced error handling code duplication by ~85% (from ~200 lines to 114 lines)
- Updated `scripts/capture.py` to use centralized error utilities
- Updated `scripts/compare.py` to use centralized error utilities  
- Updated `baseline.py` to use centralized error utilities

### Fixed
- **Panel Title Inconsistency**: Fixed mismatched summary titles between operations
- **Code Duplication**: Eliminated 8+ duplicate error handling patterns
- **Error Formatting**: Ensured consistent duration formatting (always 2 decimal places)
- **Operation Type Handling**: Added case-insensitive operation type detection

### Technical Details
- **Single Source of Truth**: All error handling now centralized in one module
- **Test Coverage**: 51 total tests now pass (26 new + 25 existing)
- **Edge Case Handling**: Comprehensive coverage for empty messages, long messages, and unknown operation types
- **Backward Compatibility**: No breaking changes - all existing functionality preserved
- **Formatting Precision**: Similarity scores and durations consistently formatted to 2 decimal places

### Improved
- **Maintainability**: All error handling logic in single module for easy updates
- **Reliability**: Consistent error output format across all CLI commands
- **Developer Experience**: Single function calls replace complex error handling blocks
- **User Experience**: Uniform error message presentation throughout application

## [0.1.1] - 2024-12-30

### Added
- Added `.github/CODEOWNERS` file to require code review for all pull requests
- All PRs now require approval from @Hiccup-za before merging

### Security
- Enhanced repository security by enforcing mandatory code reviews

## [0.1.0] - 2024-12-30

### Changed
- **BREAKING**: Refactored to unified CLI architecture with subcommands
- **BREAKING**: Changed from `python scripts/capture.py` to `python baseline.py capture`
- **BREAKING**: Changed from `python scripts/compare.py` to `python baseline.py compare`
- All arguments now use argparse validation with proper `required=True` flags
- Improved help system with subcommand-specific help messages
- Enhanced argument validation with mutually exclusive groups

### Added
- New unified `baseline.py` CLI entry point
- Subcommand architecture: `capture` and `compare` commands
- Comprehensive help system: `--help`, `capture --help`, `compare --help`
- Better argument validation and error messages
- Professional CLI structure similar to `git`, `docker`, etc.

### Fixed
- Restored comprehensive test coverage that was accidentally reduced
- Fixed argument validation to use argparse properly
- Enhanced error handling for missing required arguments
- Improved mutually exclusive argument handling

### Migration Guide
- **Old**: `python scripts/capture.py --url <URL> --name <NAME> --page`
- **New**: `python baseline.py capture --url <URL> --name <NAME> --page`
- **Old**: `python scripts/compare.py --url <URL> --name <NAME>`
- **New**: `python baseline.py compare --url <URL> --name <NAME>`

### Technical Details
- Single version number now applies to entire application, not individual scripts
- Centralized command handling in `baseline.py`
- Preserved all original functionality while improving user experience
- Enhanced test coverage for all edge cases and error conditions

## [0.0.2] - 2024-12-30

### Changed
- **BREAKING**: Refactored error handling in capture script for consistency
- Updated capture script to use "Baseline Capture Summary" consistently for all error cases
- Updated tests to match the corrected summary titles

### Fixed
- Eliminated duplicate error handling logic in `scripts/capture.py`
- Fixed inconsistent panel titles between error and success cases
- Reduced code duplication by ~70 lines through centralized error handler

### Added
- New `handle_error()` function for standardized error output formatting
- Version tracking system with `__version__.py`
- This changelog file

### Technical Details
- Created centralized error handler with consistent formatting
- Replaced 8 duplicate error handling blocks with single function calls
- Ensured capture script uses "Baseline Capture Summary" while compare script uses "Baseline Comparison Summary"
- All tests continue to pass with updated expectations

## [0.0.1] - 2024-12-30

### Added
- Initial release of baseline-cli
- Full page screenshot capture functionality
- Element-specific screenshot capture using CSS selectors and class names
- Visual comparison against baseline images
- Command-line interface with comprehensive argument validation
- Support for Chrome, Firefox, and Edge browsers
- Headless browser operation
- Rich console output with progress indicators and result summaries
- Comprehensive test suite covering CLI functionality
- GitHub Actions workflow for regression testing
- Configuration management system
- Screenshot organization in dedicated directories
- Error handling with detailed user feedback

### Features
- **Capture baseline images**: Full page or specific elements
- **Compare against baselines**: Visual regression detection
- **Multiple selector types**: CSS selectors and class names
- **Cross-browser support**: Chrome (default), Firefox, Edge
- **Configurable settings**: URLs, directories, thresholds
- **Professional output**: Rich console formatting with tables and panels
- **Robust validation**: Comprehensive CLI argument checking

### Dependencies
- Python 3.8+
- Selenium WebDriver
- OpenCV for image processing
- Rich for console output
- Pillow for image manipulation
- pytest for testing 