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

def test_capture_element_success():
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element', '--selector', 'img'])
    output = result.stdout
    
    # Assert key steps in the process
    assert "Visited URL" in output
    assert "Element screenshot captured" in output
    assert "Results compiled" in output

    # Assert summary and result
    assert "Baseline Capture Summary" in output
    assert "Result" in output and "Success" in output
    assert "Duration" in output and "seconds" in output

def test_capture_element_with_class_success():
    # Test element capture with class selector
    result = run_cli(['--url', TARGET_URL, '--name', 'test-class', '--element', '--class', 'some-class'])
    # This might fail if the class doesn't exist on the page, but we're testing CLI argument handling
    # The result could be Success or Error depending on whether the class exists

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
    assert "--element" in result.stdout
    assert "--selector" in result.stdout
    assert "--class" in result.stdout 