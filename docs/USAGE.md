# Usage Guide

## Overview

baseline-cli supports capturing and comparing visual baselines for:
- Full web pages
- Specific elements by CSS selector
- Specific elements by class name

## Capture Commands

### Full Page Capture

```bash
baseline capture --url <URL> --name <name> --page
```

**Example:**
```bash
baseline capture --url http://localhost:3000/ --name homepage --page
```

### Element Capture by CSS Selector

```bash
baseline capture --url <URL> --name <name> --element --selector "<CSS_SELECTOR>"
```

**Options:**
- `--element`: Capture a screenshot of a specific element
- `--selector`: CSS selector for the element

**Example:**
```bash
baseline capture --url http://localhost:3000/ --name button --element --selector "button"
```

### Element Capture by Class Name

```bash
baseline capture --url <URL> --name <name> --element --class "<CLASS_NAME>"
```

**Options:**
- `--class`: Class name for the element

**Example:**
```bash
baseline capture --url http://localhost:3000/ --name text-box --element --class "text-box"
```

## Compare Commands

### Full Page Comparison

```bash
baseline compare --url <URL> --name <name> --page
```

**Example:**
```bash
baseline compare --url http://localhost:3000/ --name homepage --page
```

### Element Comparison by CSS Selector

```bash
baseline compare --url <URL> --name <name> --element --selector "<CSS_SELECTOR>"
```

**Example:**
```bash
baseline compare --url http://localhost:3000/ --name button --element --selector "button"
```

### Element Comparison by Class Name

```bash
baseline compare --url <URL> --name <name> --element --class "<CLASS_NAME>"
```

**Example:**
```bash
baseline compare --url http://localhost:3000/ --name text-box --element --class "text-box"
```

## Getting Help

```bash
baseline --help                    # Show main help
baseline capture --help           # Show capture command help
baseline compare --help           # Show compare command help
```

## Common Workflows

### Setting Up a New Baseline
1. First, capture a baseline of your target:
   ```bash
   baseline capture --url http://localhost:3000/ --name my-component --element --selector ".my-component"
   ```

2. Later, compare against this baseline:
   ```bash
   baseline compare --url http://localhost:3000/ --name my-component --element --selector ".my-component"
   ```

### Batch Testing
You can create scripts to test multiple components or pages systematically by chaining commands or using shell scripts.

## Tips and Best Practices

- Use descriptive names for your baselines to make them easy to identify
- Ensure your target URLs are consistently accessible
- Configure appropriate comparison thresholds in `config/config.py`
- Regularly update baselines when intentional changes are made to your UI 