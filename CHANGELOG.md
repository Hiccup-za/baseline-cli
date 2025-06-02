# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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