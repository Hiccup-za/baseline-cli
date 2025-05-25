<p align="center">
  <img src="assets/logo.png" alt="Logo" width="100" height="100">
  <h1 align="center">baseline-cli</h1>
  <p align="center">A macOS CLI tool allows you to create visual baselines of web pages and compare them for visual regression testing</p>
</p>

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

## Features

### Capture a Baseline

Execute the following to capture a full-page screenshot and save it as a baseline image:

```sh
python scripts/capture.py --url <URL> --name <name> --page
```

> [!IMPORTANT]  
> Arguments:  
> `--url`: The URL of the page to capture (default is set in config.py)  
> `--name`: Name for the baseline image  
> `--page`: Capture a full-page screenshot  

**Example:**

```sh
$ python scripts/capture.py --url http://localhost:3000/ --name login --page

Visited URL
Screenshot captured
Results compiled

╭─ Baseline Capture Summary ─╮
│  Result    Success         │
│  Duration  3.42 seconds    │
╰────────────────────────────╯
```

### Compare against a Baseline

Execute the following to compare the current state of a website to a baseline image:

```sh
python scripts/compare.py --url <URL> --name <name>
```

> [!IMPORTANT]  
> Arguments:  
> `--url`: The URL of the page to test  
> `--name`: The name of the baseline image to compare against  

**Example:**

```sh
$ python scripts/compare.py --url http://localhost:3000/ --name login  

Visited URL
Screenshot captured
Screenshots compared
Results compiled

╭── Baseline Comparison Summary ───╮
│  Result            Success       │
│  Duration          2.01 seconds  │
│  Similarity Score  100.00%       │
╰──────────────────────────────────╯
```

## 🤝 Contributing

Coming soon...

### Dependency Overview

| Package           | Role in CLI                                                                                  |
|-------------------|---------------------------------------------------------------------------------------------|
| numpy             | Numerical operations, used by image processing libraries                                    |
| opencv-python     | Image processing and comparison                                                             |
| Pillow            | Image manipulation (cropping, saving, etc.)                                                 |
| rich              | Beautiful CLI formatting, colored output, status spinners, and tables for user feedback     |
| scikit-image      | Advanced image processing and comparison (e.g., SSIM)                                       |
| selenium          | Browser automation for screenshot capture and web interaction                                |
| urllib3           | HTTP client, required as a dependency for Selenium/webdriver-manager                        |
| webdriver-manager | Manages browser drivers for Selenium                                                        |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.