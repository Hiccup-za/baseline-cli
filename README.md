<p align="center">
  <img src="assets/logo.png" alt="Logo" width="100" height="100">
  <h1 align="center">baseline-cli</h1>
  <p align="center">A macOS CLI tool allows you to create visual baselines of web pages and elements & compare them for visual regression testing</p>
</p>

[![Regression](https://github.com/Hiccup-za/baseline-cli/actions/workflows/regression.yml/badge.svg)](https://github.com/Hiccup-za/baseline-cli/actions/workflows/regression.yml)

## 💻 Getting Started

### Prerequisites
- Python 3.8+
- Make sure ChromeDriver or the appropriate WebDriver is available
- Edit `config/config.py` to set default URLs, directories, and thresholds

### Steps

1. Create and activate the virtual environment
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies  
    ```
    pip install -r requirements.txt
    ```
    
> [!TIP]  
> Deactivate the virtual environment when done:
> ```
> deactivate
> ```

## ✨ Features

### Capture a Baseline

You can capture a baseline of:
- The full page
- A specific element by CSS selector
- A specific element by class name

#### Full Page

```sh
python scripts/capture.py --url <URL> --name <name> --page
```

#### Element by CSS Selector

```sh
python scripts/capture.py --url <URL> --name <name> --element --selector "<CSS_SELECTOR>"
```
- `--element`: Capture a screenshot of a specific element
- `--selector`: CSS selector for the element

#### Element by Class Name

```sh
python scripts/capture.py --url <URL> --name <name> --element --class "<CLASS_NAME>"
```
- `--class`: Class name for the element

**Examples:**

```sh
python scripts/capture.py --url http://localhost:3000/ --name button --element --selector "button"
python scripts/capture.py --url http://localhost:3000/ --name text-box --element --class "text-box"
```

### Compare against a Baseline

You can compare:
- The full page
- A specific element by CSS selector
- A specific element by class name

#### Full Page

```sh
python scripts/compare.py --url <URL> --name <name> --page
```

#### Element by CSS Selector

```sh
python scripts/compare.py --url <URL> --name <name> --element --selector "<CSS_SELECTOR>"
```

#### Element by Class Name

```sh
python scripts/compare.py --url <URL> --name <name> --element --class "<CLASS_NAME>"
```

**Examples:**

```sh
python scripts/compare.py --url http://localhost:3000/ --name button --element --selector "button"
python scripts/compare.py --url http://localhost:3000/ --name text-box --element --class "text-box"
```

## 🧪 Tests

Automated tests are provided in the `tests/` directory, which cover the main CLI functionality:  
- Baseline capture (full page and element)
- Baseline comparison
- CLI argument validation and error handling

To run all tests, activate your virtual environment and run:

```sh
pytest tests/
```

## 🤝 Contributing

Want to contribute?  
Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.