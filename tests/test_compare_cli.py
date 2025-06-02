import subprocess
import sys
import os
import pytest
from config.config import TARGET_URL

def run_cli(args):
    result = subprocess.run(
        ['baseline', 'compare'] + args,
        capture_output=True,
        text=True
    )
    return result

def test_baseline_success():
    # Ensure the baseline image exists before running this test
    from config.config import BASELINE_DIR
    baseline_path = os.path.join(BASELINE_DIR, "login_baseline.png")
    if not os.path.exists(baseline_path):
        pytest.skip("Baseline image does not exist.")
    result = run_cli(['--url', TARGET_URL, '--name', 'login'])
    output = result.stdout

    # Assert key steps in the process
    assert "Visited URL" in output
    assert "Screenshot captured" in output
    assert "Screenshots compared" in output
    assert "Results compiled" in output

    # Assert summary and result
    assert "Baseline Comparison Summary" in output
    assert "Result" in output and "Success" in output
    assert "Duration" in output
    assert "Similarity Score" in output and "100.00%" in output

def test_baseline_with_page_flag():
    # Test explicit --page flag (should be default anyway)
    from config.config import BASELINE_DIR
    baseline_path = os.path.join(BASELINE_DIR, "login_baseline.png")
    if not os.path.exists(baseline_path):
        pytest.skip("Baseline image does not exist.")
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--page'])
    output = result.stdout
    assert "Baseline Comparison Summary" in output

def test_baseline_image_not_found():
    result = run_cli(['--url', TARGET_URL, '--name', 'nonexistent'])
    assert "Image not found" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_element_missing_selector_and_class():
    # Test --element without --selector or --class
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element'])
    # Should show error message about requiring --class or --selector
    assert "You must provide either --class or --selector for --element" in result.stdout

def test_element_with_both_selector_and_class():
    # Test --element with both --selector and --class (should be mutually exclusive)
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element', '--selector', 'img', '--class', 'some-class'])
    assert result.returncode == 2  # argparse error code
    assert "not allowed" in result.stderr or "mutually exclusive" in result.stderr

def test_missing_url_argument():
    # Test missing --url argument entirely
    result = run_cli(['--name', 'login'])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and "--url" in result.stderr

def test_missing_name_argument():
    # Test missing --name argument entirely
    result = run_cli(['--url', TARGET_URL])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and "--name" in result.stderr

def test_both_page_and_element_provided():
    # Test providing both --page and --element (should be mutually exclusive)
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--page', '--element', '--selector', 'img'])
    assert result.returncode == 2  # argparse error code
    assert "not allowed" in result.stderr or "mutually exclusive" in result.stderr

def test_help_message():
    # Test that help works for compare command
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert "Compare current screenshots against baseline images" in result.stdout
    assert "--url" in result.stdout
    assert "--name" in result.stdout
    assert "--page" in result.stdout
    assert "--element" in result.stdout
