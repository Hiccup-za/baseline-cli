import subprocess
import sys
import os
import pytest

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'capture.py')

def run_cli(args):
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH] + args,
        capture_output=True,
        text=True
    )
    return result

def test_name_not_provided_error():
    result = run_cli(['--url', 'http://localhost:3000/', '--page', '--name'])
    assert "Baseline name not provided" in result.stdout
    assert "Baseline Comparison Summary" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_name_arg_not_provided_error():
    result = run_cli(['--url', 'http://localhost:3000/', '--page'])
    assert "The --name arg was not provided" in result.stdout
    assert "Baseline Comparison Summary" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_url_not_provided_error():
    result = run_cli(['--url', '--page', '--name', 'login'])
    assert "URL not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_url_arg_not_provided_error():
    result = run_cli(['--page', '--name', 'login'])
    assert "The --url arg was not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_type_arg_not_provided_error():
    result = run_cli(['--url', 'http://localhost:3000/', '--name', 'login'])
    assert "The --page or --element arg was not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 
