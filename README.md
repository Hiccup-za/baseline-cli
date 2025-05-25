# baseline-cli

## Baseline Creation and Comparison

This CLI tool allows you to create visual baselines of web pages and compare them for visual regression testing.

---

## Setting Up a Python Virtual Environment

It is recommended to use a Python virtual environment to manage dependencies and avoid conflicts with system packages.

### 1. Create and Activate the Virtual Environment (macOS)
```
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Deactivate the Virtual Environment When Done
```
deactivate
```

---

## 1. Creating a Baseline

To create a baseline screenshot or element template, use the script:
 
```
python scripts/capture.py --url <URL> --page --name <baseline_name>
```
- This will save a full-page screenshot as a baseline.

To capture a specific element as a template:
```
python scripts/capture.py --url <URL> --element --name <template_name> --selector '<CSS_SELECTOR>'
```

**Arguments:**
- `--url`: The URL of the page to capture (default is set in config.py)
- `--page`: Capture a full-page screenshot
- `--element`: Capture a specific element
- `--name`: Name for the baseline/template image
- `--selector`: CSS selector for the element (required for --element)

---

## 2. Comparing a Screenshot to a Baseline

To compare the current state of a website to a baseline image, use:

```
python scripts/compare.py --url <URL> --name <name>
```
- This will navigate to the URL, take a screenshot, and compare it to the baseline image (e.g., `baseline_name_baseline.png` in your baseline directory, where `baseline_name` matches the name you used during capture).
- The script will print the similarity score and output a diff image if differences are found.

**Arguments:**
- `--url`: The URL of the page to test
- `--name`: The name of the baseline image to compare against (should match the name used during capture, without extension)

**Example:**
```
python scripts/compare.py --url https://your-website.com --name homepage
```

---

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies (selenium, pillow, opencv-python, scikit-image, webdriver-manager, etc.)

---

## Dependency Overview

| Package           | Role in CLI                                                                                  |
|-------------------|---------------------------------------------------------------------------------------------|
| selenium          | Browser automation for screenshot capture and web interaction                                |
| webdriver-manager | Manages browser drivers for Selenium                                                        |
| opencv-python     | Image processing and comparison                                                             |
| numpy             | Numerical operations, used by image processing libraries                                    |
| Pillow            | Image manipulation (cropping, saving, etc.)                                                 |
| scikit-image      | Advanced image processing and comparison (e.g., SSIM)                                       |
| urllib3           | HTTP client, required as a dependency for Selenium/webdriver-manager                        |

---

## Configuration
- Edit `config/config.py` to set default URLs, directories, and thresholds as needed.

---

## Notes
- Make sure ChromeDriver or the appropriate WebDriver is available (the scripts use `webdriver-manager` to auto-install drivers).
- Baseline images are stored in the directory specified in `config.py` (e.g., `BASELINE_DIR`).
- Diff images and results are stored in their respective directories as configured.