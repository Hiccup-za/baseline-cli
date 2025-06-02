import subprocess
import sys
import os
import pytest
from config.config import TARGET_URL

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'capture.py')

def run_cli(args):
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH] + args,
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

def test_name_not_provided_error():
    result = run_cli(['--url', TARGET_URL, '--element', '--name'])
    assert "Baseline name not provided" in result.stdout
    assert "Baseline Capture Summary" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_name_arg_not_provided_error():
    result = run_cli(['--url', TARGET_URL, '--element'])
    assert "The --name arg was not provided" in result.stdout
    assert "Baseline Capture Summary" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_url_not_provided_error():
    result = run_cli(['--url', '--element', '--name', 'login'])
    assert "URL not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_url_arg_not_provided_error():
    result = run_cli(['--element', '--name', 'login'])
    assert "The --url arg was not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_element_selector_not_provided_error():
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element', '--selector'])
    assert "Selector not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_element_class_not_provided_error():
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element', '--class'])
    assert "Class not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_element_class_arg_not_provided_error():
    result = run_cli(['--url', TARGET_URL, '--name', 'login', '--element'])
    assert "You must provide either --class or --selector for --element" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_type_arg_not_provided_error():
    result = run_cli(['--url', TARGET_URL, '--name', 'login'])
    assert "The --page or --element arg was not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 
