<p align="center">
  <img src="assets/logo.png" alt="Logo" width="100" height="100">
  <h1 align="center">baseline-cli</h1>
  <p align="center">A macOS CLI tool for creating visual baselines of web pages and elements & comparing them for visual regression testing</p>
</p>

[![Regression](https://github.com/Hiccup-za/baseline-cli/actions/workflows/regression.yml/badge.svg)](https://github.com/Hiccup-za/baseline-cli/actions/workflows/regression.yml)

## 🚀 Quick Start

### Installation

```bash
# Install in development mode (from project directory)
pip install -e .
```

### Basic Usage

```bash
# Capture a baseline
baseline capture --url http://localhost:3000/ --name homepage --page

# Compare against baseline
baseline compare --url http://localhost:3000/ --name homepage --page
```

## 📚 Documentation

| Topic | Description |
|-------|-------------|
| **[Installation](docs/INSTALLATION.md)** | Complete setup guide, prerequisites, and configuration |
| **[Usage Guide](docs/USAGE.md)** | Detailed commands, examples, and best practices |
| **[Testing](docs/TESTING.md)** | Running tests, writing new tests, and CI information |

## ✨ Key Features

- **Full Page Capture**: Screenshot entire web pages for comprehensive testing
- **Element-Specific Testing**: Target specific elements using CSS selectors or class names
- **Visual Comparison**: Automated diff generation to highlight changes
- **CLI Interface**: Simple command-line interface for easy integration
- **Configurable Thresholds**: Customizable sensitivity for change detection

## 💻 Requirements

- Python 3.8+
- ChromeDriver or appropriate WebDriver
- macOS (primary platform)

## 🔧 Quick Commands

```bash
# Get help
baseline --help

# Check version
baseline --version

# Capture examples
baseline capture --url <URL> --name <name> --page
baseline capture --url <URL> --name <name> --element --selector "button"

# Compare examples  
baseline compare --url <URL> --name <name> --page
baseline compare --url <URL> --name <name> --element --class "text-box"
```

## 🤝 Contributing

Want to contribute? Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes and version releases.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.