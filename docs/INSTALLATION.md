# Installation Guide

## Prerequisites
- Python 3.8+
- Make sure ChromeDriver or the appropriate WebDriver is available
- Edit `config/config.py` to set default URLs, directories, and thresholds

## Installation Steps

### Option 1: Development Installation (Recommended)

For development or if you're cloning the repository:

```bash
# 1. Clone the repository
git clone https://github.com/Hiccup-za/baseline-cli.git
cd baseline-cli

# 2. Create and activate virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# 3. Install in development mode - this makes the 'baseline' command available
pip install -e .
```

### Option 2: Direct Installation from Source

```bash
# Install directly from the repository
pip install git+https://github.com/Hiccup-za/baseline-cli.git
```

> [!TIP]  
> Deactivate the virtual environment when done:
> ```bash
> deactivate
> ```

## Verification

After installation, verify that baseline-cli is working:

```bash
# Check version
baseline --version

# Get help
baseline --help
```

## Configuration

Before using baseline-cli, make sure to configure your settings:

1. Navigate to `config/config.py`
2. Set your default URLs, directories, and comparison thresholds
3. Adjust any other settings as needed for your environment

## Troubleshooting

If you encounter issues during installation:

1. **Python version**: Ensure you're using Python 3.8 or higher
2. **Virtual environment**: Make sure your virtual environment is activated
3. **Dependencies**: Try upgrading pip before installing requirements: `pip install --upgrade pip`
4. **WebDriver**: Ensure ChromeDriver is properly installed and in your PATH
5. **Command not found**: If `baseline` command is not found, ensure the installation completed successfully and try restarting your terminal