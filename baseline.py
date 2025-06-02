#!/usr/bin/env python3
"""
Main CLI entry point for baseline-cli.

This is the unified command-line interface for visual regression testing.
Run 'baseline --help' for usage information.
"""
import os
import sys
import argparse
from rich.console import Console

# Add project root to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from __version__ import __version__, __title__, __description__

console = Console()

def main():
    """Main CLI entry point with subcommands."""
    parser = argparse.ArgumentParser(
        prog='baseline-cli',
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {sys.argv[0]} capture --url http://localhost:3000 --name homepage --page
  {sys.argv[0]} capture --url http://localhost:3000 --name button --element --selector "button"
  {sys.argv[0]} compare --url http://localhost:3000 --name homepage --page
  {sys.argv[0]} --version

For more help on a specific command:
  {sys.argv[0]} capture --help
  {sys.argv[0]} compare --help
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'{__title__} v{__version__}'
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='command'
    )
    
    # Capture subcommand
    capture_parser = subparsers.add_parser(
        'capture',
        help='Capture baseline screenshots',
        description='Capture baseline screenshots of web pages or elements'
    )
    capture_parser.add_argument('--url', type=str, required=True, help='URL to navigate to')
    capture_parser.add_argument('--name', type=str, required=True, help='Name for the baseline/template')
    
    capture_group = capture_parser.add_mutually_exclusive_group(required=True)
    capture_group.add_argument('--page', action='store_true', help='Capture full page screenshot')
    capture_group.add_argument('--element', action='store_true', help='Capture element template')
    
    element_group = capture_parser.add_mutually_exclusive_group()
    element_group.add_argument('--class', dest='class_name', type=str, help='Class name for the element (required with --element)')
    element_group.add_argument('--selector', dest='css_selector', type=str, help='CSS selector for the element (required with --element)')
    
    # Compare subcommand
    compare_parser = subparsers.add_parser(
        'compare',
        help='Compare against baseline images',
        description='Compare current screenshots against baseline images'
    )
    compare_parser.add_argument('--url', type=str, required=True, help='URL to test')
    compare_parser.add_argument('--name', type=str, required=True, help='Name of the baseline image (without extension)')
    
    compare_group = compare_parser.add_mutually_exclusive_group()
    compare_group.add_argument('--page', action='store_true', help='Compare full page screenshot (default)')
    compare_group.add_argument('--element', action='store_true', help='Compare element screenshot')
    
    compare_element_group = compare_parser.add_mutually_exclusive_group()
    compare_element_group.add_argument('--class', dest='class_name', type=str, help='Class name for the element (used with --element)')
    compare_element_group.add_argument('--selector', dest='css_selector', type=str, help='CSS selector for the element (used with --element)')
    
    args = parser.parse_args()
    
    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return
    
    # Import and execute the appropriate command
    if args.command == 'capture':
        from scripts.capture import capture_full_page_baseline, capture_element_template
        from utils.web_utils import create_driver
        from utils.error_utils import handle_cli_error, display_success_summary
        from config.config import HEADLESS, BASELINE_DIR
        from selenium.webdriver.common.by import By
        
        # Validate element-specific arguments
        if args.element and not args.class_name and not args.css_selector:
            handle_cli_error("You must provide either --class or --selector for --element", operation_type="capture")
        
        os.makedirs(BASELINE_DIR, exist_ok=True)
        driver = create_driver(headless=HEADLESS)
        
        try:
            if args.page:
                result, output_path, duration = capture_full_page_baseline(args.url, args.name, driver, should_quit=False)
            elif args.element:
                if args.class_name:
                    result, output_path, duration = capture_element_template(args.url, args.class_name, args.name, selector_type=By.CLASS_NAME, driver=driver, should_quit=False)
                elif args.css_selector:
                    result, output_path, duration = capture_element_template(args.url, args.css_selector, args.name, selector_type=By.CSS_SELECTOR, driver=driver, should_quit=False)
        finally:
            driver.quit()
            
        # Display results using consolidated success summary
        display_success_summary(result, duration, operation_type="capture")
    
    elif args.command == 'compare':
        from scripts.compare import compare_website_visuals
        from utils.error_utils import handle_cli_error, display_success_summary
        
        # Validate element-specific arguments
        if args.element and not args.class_name and not args.css_selector:
            handle_cli_error("You must provide either --class or --selector for --element", operation_type="compare")
        
        # Execute comparison
        if args.element:
            result, similarity_score, duration = compare_website_visuals(
                args.url, args.name, 
                compare_element=True, 
                class_name=args.class_name, 
                css_selector=args.css_selector
            )
        else:
            result, similarity_score, duration = compare_website_visuals(
                args.url, args.name, 
                compare_element=False
            )
        
        # Display results using consolidated success summary
        display_success_summary(result, duration, similarity_score, operation_type="compare")

if __name__ == "__main__":
    main() 