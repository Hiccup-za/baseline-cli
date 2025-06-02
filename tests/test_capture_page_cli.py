import subprocess
import sys
import os
import pytest
from config.config import TARGET_URL

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'baseline.py')

def run_cli(args):
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH] + ['capture'] + args,
        capture_output=True,
        text=True
    )
    return result

def test_capture_page_success():
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--page'])
    output = result.stdout
    
    # Assert key steps in the process
    assert "Visited URL" in output
    assert "Screenshot captured" in output
    assert "Results compiled" in output

    # Assert summary and result
    assert "Baseline Capture Summary" in output
    assert "Result" in output and "Success" in output
    assert "Duration" in output and "seconds" in output

def test_missing_url_argument():
    # Test missing --url argument entirely
    result = run_cli(['--name', 'login', '--page'])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and "--url" in result.stderr

def test_missing_name_argument():
    # Test missing --name argument entirely  
    result = run_cli(['--url', TARGET_URL, '--page'])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and "--name" in result.stderr

def test_missing_page_element_argument():
    # Test missing --page or --element argument
    result = run_cli(['--url', TARGET_URL, '--name', 'login'])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and ("--page" in result.stderr or "--element" in result.stderr)

def test_both_page_and_element_provided():
    # Test providing both --page and --element (should be mutually exclusive)
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--page', '--element', '--selector', 'button'])
    assert result.returncode == 2  # argparse error code
    assert "not allowed" in result.stderr or "mutually exclusive" in result.stderr

def test_element_without_selector_or_class():
    # Test --element without --selector or --class
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element'])
    # This should pass argparse validation but fail our custom validation
    assert "You must provide either --class or --selector for --element" in result.stdout

def test_element_with_both_selector_and_class():
    # Test --element with both --selector and --class (should be mutually exclusive)
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element', '--selector', 'button', '--class', 'btn'])
    assert result.returncode == 2  # argparse error code
    assert "not allowed" in result.stderr or "mutually exclusive" in result.stderr

def test_help_message():
    # Test that help works
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert "Capture baseline screenshots" in result.stdout
    assert "--url" in result.stdout
    assert "--name" in result.stdout
    assert "--page" in result.stdout
    assert "--element" in result.stdout
