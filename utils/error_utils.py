"""
Error handling utilities for baseline-cli.

This module provides consistent error handling and output formatting
across all CLI commands and scripts.
"""
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def handle_cli_error(message, operation_type="capture", duration=0.0, result="Failed", exit_code=1):
    """
    Handle CLI errors with consistent formatting and exit behavior.
    
    Args:
        message (str): Error message to display
        operation_type (str): Type of operation ("capture" or "compare")
        duration (float): Duration of the operation before error
        result (str): Result status ("Failed", "Error", "Cancelled")
        exit_code (int): Exit code to use when calling sys.exit()
    """
    # Determine the appropriate panel title based on operation type
    if operation_type.lower() == "compare":
        panel_title = "Baseline Comparison Summary"
    else:
        panel_title = "Baseline Capture Summary"
    
    # Print error message
    console.print()
    console.print(f"[bold red]{message}")
    
    # Create and display summary table
    table = Table(show_header=False, box=None)
    table.add_row("Result", result)
    table.add_row("Duration", f"{duration:.2f} seconds")
    console.print()
    console.print(Panel(table, title=panel_title, expand=False))
    
    sys.exit(exit_code)

def handle_multiple_cli_errors(messages, operation_type="capture", duration=0.0, result="Failed", exit_code=1):
    """
    Handle multiple CLI errors with consistent formatting.
    
    Args:
        messages (list): List of error messages to display
        operation_type (str): Type of operation ("capture" or "compare")
        duration (float): Duration of the operation before error
        result (str): Result status ("Failed", "Error", "Cancelled")
        exit_code (int): Exit code to use when calling sys.exit()
    """
    # Determine the appropriate panel title based on operation type
    if operation_type.lower() == "compare":
        panel_title = "Baseline Comparison Summary"
    else:
        panel_title = "Baseline Capture Summary"
    
    # Print all error messages
    console.print()
    for message in messages:
        console.print(f"[bold red]{message}")
    
    # Create and display summary table
    table = Table(show_header=False, box=None)
    table.add_row("Result", result)
    table.add_row("Duration", f"{duration:.2f} seconds")
    console.print()
    console.print(Panel(table, title=panel_title, expand=False))
    
    sys.exit(exit_code)

def format_function_error(message, duration=0.0, result="Failed"):
    """
    Format error for function return (non-exit scenarios).
    
    Args:
        message (str): Error message to display
        duration (float): Duration of the operation before error
        result (str): Result status ("Failed", "Error", "Cancelled")
    
    Returns:
        tuple: (result, None, duration) matching the expected return format
    """
    console.print(f"\n[bold red]{message}")
    return result, None, duration

def display_success_summary(result, duration, similarity_score=None, operation_type="capture"):
    """
    Display success summary with consistent formatting.
    
    Args:
        result (str): Result status ("Success")
        duration (float): Duration of the operation
        similarity_score (float, optional): Similarity score for comparisons
        operation_type (str): Type of operation ("capture" or "compare")
    """
    # Determine the appropriate panel title based on operation type
    if operation_type.lower() == "compare":
        panel_title = "Baseline Comparison Summary"
    else:
        panel_title = "Baseline Capture Summary"
    
    table = Table(show_header=False, box=None)
    table.add_row("Result", result)
    table.add_row("Duration", f"{duration:.2f} seconds")
    
    if similarity_score is not None:
        table.add_row("Similarity Score", f"{similarity_score * 100:.2f}%")
    
    console.print()
    console.print(Panel(table, title=panel_title, expand=False)) 