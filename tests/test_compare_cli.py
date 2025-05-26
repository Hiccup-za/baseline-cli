import subprocess
import sys
import os
import pytest
import re

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'compare.py')
TEST_URL = 'https://baseline-website.vercel.app/'

def run_cli(args):
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH] + args,
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
    result = run_cli(['--url', TEST_URL, '--name', 'login'])
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

def test_baseline_image_not_found():
    result = run_cli(['--url', TEST_URL, '--name', 'nonexistent'])
    assert "Image not found" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_baseline_image_not_provided():
    result = run_cli(['--url', TEST_URL, '--name'])
    assert "Image name not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_baseline_image_arg_not_provided():
    result = run_cli(['--url', TEST_URL])
    assert "The --name arg was not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_baseline_url_not_provided():
    result = run_cli(['--url', '--name', 'login'])
    assert "URL not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_baseline_url_arg_not_provided():
    result = run_cli(['--name', 'login'])
    assert "The --url arg was not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 

def test_baseline_args_not_provided():
    result = run_cli([])
    assert "The --url arg was not provided" in result.stdout
    assert "The --name arg was not provided" in result.stdout
    assert "Result" in result.stdout and "Failed" in result.stdout 
    assert "Duration" in result.stdout and "0.00 seconds" in result.stdout 
