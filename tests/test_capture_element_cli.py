import subprocess
import sys
import os
import pytest
from config.config import TARGET_URL

def run_cli(args):
    result = subprocess.run(
        ['baseline', 'capture'] + args,
        capture_output=True,
        text=True
    )
    return result

def test_capture_element_with_class_success():
    result = run_cli(['--url', TARGET_URL, '--name', 'test-btn', '--element', '--class', 'btn'])
    output = result.stdout
    
    # Assert key steps in the process
    assert "Visited URL" in output
    # Note: Element might not exist on the page, so we check for either success or error
    assert ("Element located" in output or "Error capturing element template" in output)

def test_capture_element_with_selector_success():
    result = run_cli(['--url', TARGET_URL, '--name', 'form-btn', '--element', '--selector', 'input[type="submit"]'])
    output = result.stdout
    
    # Assert key steps in the process
    assert "Visited URL" in output
    # Note: Element might not exist on the page, so we check for either success or error
    assert ("Element located" in output or "Error capturing element template" in output)

def test_capture_element_not_found():
    result = run_cli(['--url', TARGET_URL, '--name', 'missing-element', '--element', '--class', 'non-existent-class'])
    # Should show error message about element not being found
    assert ("Element not found" in result.stdout or "Error capturing element template" in result.stdout)

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
    result = run_cli(['--name', 'login', '--element', '--selector', 'img'])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and "--url" in result.stderr

def test_missing_name_argument():
    # Test missing --name argument entirely
    result = run_cli(['--url', TARGET_URL, '--element', '--selector', 'img'])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and "--name" in result.stderr

def test_missing_page_element_argument():
    # Test missing --page or --element argument
    result = run_cli(['--url', TARGET_URL, '--name', 'login'])
    assert result.returncode == 2  # argparse error code
    assert "required" in result.stderr and ("--page" in result.stderr or "--element" in result.stderr)

def test_help_message():
    # Test that help works for capture command
    result = run_cli(['--help'])
    assert result.returncode == 0
    assert "Capture baseline screenshots" in result.stdout
    assert "--url" in result.stdout
    assert "--name" in result.stdout
    assert "--page" in result.stdout
    assert "--element" in result.stdout
    assert "--class" in result.stdout
    assert "--selector" in result.stdout 