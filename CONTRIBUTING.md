# Contributing to baseline-cli

Thank you for your interest in contributing to baseline-cli!  
This page will guide you through the process of contributing to the project.

## Steps

### Repo setup

- Fork the repository
- Clone your fork locally & create a new branch for your feature/fix
- Follow the [README.md](README.md) to set up the project

> [!WARNING]  
> Always keep your fork up to date with the main repository to avoid conflicts.

### Making changes

- Make your changes, commit them & push your branch to your fork
- Ensure all tests pass and add new tests if you extend functionality

### Pull request process

- Open a pull request describing your changes
- Wait for review and address any feedback

## Dependency Overview

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

## License
By contributing to baseline-cli, you agree that your contributions will be licensed under its MIT License.