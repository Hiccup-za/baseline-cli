# Testing Documentation

## Overview

baseline-cli includes comprehensive automated tests to ensure reliability and functionality. The test suite covers:
- Baseline capture (full page and element)
- Baseline comparison
- CLI argument validation and error handling

## Running Tests

### Run All Tests

To run the complete test suite:

```bash
pytest tests/
```

### Run Specific Test Files

To run tests from a specific file:

```bash
pytest tests/test_specific_file.py
```

### Run Tests with Verbose Output

For detailed output during test execution:

```bash
pytest tests/ -v
```

## Test Structure

The tests are organized in the `tests/` directory and cover:

- **CLI Interface Tests**: Validate command-line argument parsing and help output
- **Capture Functionality Tests**: Ensure baseline capture works for pages and elements
- **Comparison Tests**: Verify that visual comparisons work correctly
- **Error Handling Tests**: Test various error conditions and edge cases

## Test Requirements

Before running tests, ensure:

1. Your virtual environment is activated
2. All dependencies are installed (`pip install -r requirements.txt`)
3. Test dependencies are available (included in requirements.txt)

## Continuous Integration

This project uses GitHub Actions for automated testing. The test suite runs automatically on:
- Pull requests
- Pushes to main branch
- Scheduled intervals

See the regression badge in the main README for current test status.

## Writing New Tests

When contributing new features:

1. Add corresponding tests in the `tests/` directory
2. Follow the existing test naming conventions
3. Ensure tests are isolated and don't depend on external services
4. Include both positive and negative test cases
5. Test edge cases and error conditions

## Test Coverage

To check test coverage:

```bash
pytest tests/ --cov=baseline
```

This will show which parts of the code are covered by tests and highlight areas that might need additional testing. 