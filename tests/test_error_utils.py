"""
Test suite for error handling utilities.

This module tests all error handling functions to ensure consistent
behavior and output formatting across different scenarios.
"""
import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add project root to path
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_utils import (
    handle_cli_error,
    handle_multiple_cli_errors,
    format_function_error,
    display_success_summary
)


class TestHandleCliError:
    """Test the handle_cli_error function."""
    
    def test_handle_cli_error_capture_operation(self, capsys):
        """Test handle_cli_error with capture operation type."""
        with pytest.raises(SystemExit) as exc_info:
            handle_cli_error("Test error message", operation_type="capture")
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        
        # Check that error message is displayed
        assert "Test error message" in captured.out
        assert "Baseline Capture Summary" in captured.out
        assert "Result" in captured.out
        assert "Failed" in captured.out
        assert "Duration" in captured.out
        assert "0.00 seconds" in captured.out
    
    def test_handle_cli_error_compare_operation(self, capsys):
        """Test handle_cli_error with compare operation type."""
        with pytest.raises(SystemExit) as exc_info:
            handle_cli_error("Test error message", operation_type="compare")
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        
        # Check that correct panel title is used
        assert "Test error message" in captured.out
        assert "Baseline Comparison Summary" in captured.out
        assert "Result" in captured.out
        assert "Failed" in captured.out
    
    def test_handle_cli_error_custom_parameters(self, capsys):
        """Test handle_cli_error with custom parameters."""
        with pytest.raises(SystemExit) as exc_info:
            handle_cli_error(
                "Custom error",
                operation_type="capture",
                duration=2.5,
                result="Error",
                exit_code=2
            )
        
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        
        assert "Custom error" in captured.out
        assert "Error" in captured.out
        assert "2.50 seconds" in captured.out
    
    def test_handle_cli_error_default_operation_type(self, capsys):
        """Test handle_cli_error with default operation type."""
        with pytest.raises(SystemExit):
            handle_cli_error("Default test")
        
        captured = capsys.readouterr()
        # Should default to capture operation
        assert "Baseline Capture Summary" in captured.out
    
    def test_handle_cli_error_case_insensitive_operation(self, capsys):
        """Test handle_cli_error with case variations in operation type."""
        with pytest.raises(SystemExit):
            handle_cli_error("Test", operation_type="COMPARE")
        
        captured = capsys.readouterr()
        assert "Baseline Comparison Summary" in captured.out
        
        with pytest.raises(SystemExit):
            handle_cli_error("Test", operation_type="Compare")
        
        captured = capsys.readouterr()
        assert "Baseline Comparison Summary" in captured.out


class TestHandleMultipleCliErrors:
    """Test the handle_multiple_cli_errors function."""
    
    def test_handle_multiple_cli_errors_basic(self, capsys):
        """Test handle_multiple_cli_errors with multiple messages."""
        messages = ["First error", "Second error", "Third error"]
        
        with pytest.raises(SystemExit) as exc_info:
            handle_multiple_cli_errors(messages, operation_type="compare")
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        
        # Check all error messages are displayed
        for message in messages:
            assert message in captured.out
        
        assert "Baseline Comparison Summary" in captured.out
        assert "Failed" in captured.out
    
    def test_handle_multiple_cli_errors_single_message(self, capsys):
        """Test handle_multiple_cli_errors with single message in list."""
        messages = ["Single error message"]
        
        with pytest.raises(SystemExit):
            handle_multiple_cli_errors(messages, operation_type="capture")
        
        captured = capsys.readouterr()
        assert "Single error message" in captured.out
        assert "Baseline Capture Summary" in captured.out
    
    def test_handle_multiple_cli_errors_empty_list(self, capsys):
        """Test handle_multiple_cli_errors with empty message list."""
        with pytest.raises(SystemExit):
            handle_multiple_cli_errors([], operation_type="capture")
        
        captured = capsys.readouterr()
        # Should still show summary table even with no error messages
        assert "Baseline Capture Summary" in captured.out
        assert "Failed" in captured.out
    
    def test_handle_multiple_cli_errors_custom_parameters(self, capsys):
        """Test handle_multiple_cli_errors with custom parameters."""
        messages = ["Error 1", "Error 2"]
        
        with pytest.raises(SystemExit) as exc_info:
            handle_multiple_cli_errors(
                messages,
                operation_type="compare",
                duration=1.25,
                result="Cancelled",
                exit_code=3
            )
        
        assert exc_info.value.code == 3
        captured = capsys.readouterr()
        
        assert "Error 1" in captured.out
        assert "Error 2" in captured.out
        assert "Cancelled" in captured.out
        assert "1.25 seconds" in captured.out


class TestFormatFunctionError:
    """Test the format_function_error function."""
    
    def test_format_function_error_basic(self, capsys):
        """Test format_function_error with basic parameters."""
        result, output, duration = format_function_error("Function error message")
        
        assert result == "Failed"
        assert output is None
        assert duration == 0.0
        
        captured = capsys.readouterr()
        assert "Function error message" in captured.out
    
    def test_format_function_error_custom_parameters(self, capsys):
        """Test format_function_error with custom parameters."""
        result, output, duration = format_function_error(
            "Custom function error",
            duration=3.75,
            result="Error"
        )
        
        assert result == "Error"
        assert output is None
        assert duration == 3.75
        
        captured = capsys.readouterr()
        assert "Custom function error" in captured.out
    
    def test_format_function_error_no_exit(self):
        """Test that format_function_error doesn't call sys.exit."""
        # This should not raise SystemExit
        result, output, duration = format_function_error("No exit test")
        assert result == "Failed"
        assert output is None
        assert duration == 0.0


class TestDisplaySuccessSummary:
    """Test the display_success_summary function."""
    
    def test_display_success_summary_capture_without_score(self, capsys):
        """Test display_success_summary for capture operation without similarity score."""
        display_success_summary("Success", 2.5, operation_type="capture")
        
        captured = capsys.readouterr()
        assert "Baseline Capture Summary" in captured.out
        assert "Success" in captured.out
        assert "2.50 seconds" in captured.out
        # Should not contain similarity score
        assert "Similarity Score" not in captured.out
    
    def test_display_success_summary_compare_with_score(self, capsys):
        """Test display_success_summary for compare operation with similarity score."""
        display_success_summary("Success", 1.75, similarity_score=0.95, operation_type="compare")
        
        captured = capsys.readouterr()
        assert "Baseline Comparison Summary" in captured.out
        assert "Success" in captured.out
        assert "1.75 seconds" in captured.out
        assert "Similarity Score" in captured.out
        assert "95.00%" in captured.out
    
    def test_display_success_summary_failed_result(self, capsys):
        """Test display_success_summary with failed result."""
        display_success_summary("Failed", 0.5, similarity_score=0.75, operation_type="compare")
        
        captured = capsys.readouterr()
        assert "Failed" in captured.out
        assert "75.00%" in captured.out
    
    def test_display_success_summary_default_operation_type(self, capsys):
        """Test display_success_summary with default operation type."""
        display_success_summary("Success", 1.0)
        
        captured = capsys.readouterr()
        # Should default to capture
        assert "Baseline Capture Summary" in captured.out
    
    def test_display_success_summary_zero_similarity_score(self, capsys):
        """Test display_success_summary with zero similarity score."""
        display_success_summary("Failed", 1.0, similarity_score=0.0, operation_type="compare")
        
        captured = capsys.readouterr()
        assert "0.00%" in captured.out
    
    def test_display_success_summary_high_precision_score(self, capsys):
        """Test display_success_summary with high precision similarity score."""
        display_success_summary("Success", 1.0, similarity_score=0.987654, operation_type="compare")
        
        captured = capsys.readouterr()
        assert "98.77%" in captured.out  # Should round to 2 decimal places


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_error_message(self, capsys):
        """Test behavior with empty error message."""
        with pytest.raises(SystemExit):
            handle_cli_error("", operation_type="capture")
        
        captured = capsys.readouterr()
        # Should still show summary even with empty message
        assert "Baseline Capture Summary" in captured.out
    
    def test_very_long_error_message(self, capsys):
        """Test behavior with very long error message."""
        long_message = "This is a very long error message " * 10
        
        with pytest.raises(SystemExit):
            handle_cli_error(long_message, operation_type="capture")
        
        captured = capsys.readouterr()
        # Check for parts of the message since Rich may wrap long text
        assert "This is a very long error message" in captured.out
        assert "Baseline Capture Summary" in captured.out
    
    def test_unknown_operation_type(self, capsys):
        """Test behavior with unknown operation type."""
        with pytest.raises(SystemExit):
            handle_cli_error("Test", operation_type="unknown")
        
        captured = capsys.readouterr()
        # Should default to capture summary for unknown operation types
        assert "Baseline Capture Summary" in captured.out
    
    def test_negative_duration(self, capsys):
        """Test behavior with negative duration."""
        display_success_summary("Success", -1.5, operation_type="capture")
        
        captured = capsys.readouterr()
        assert "-1.50 seconds" in captured.out
    
    def test_very_large_duration(self, capsys):
        """Test behavior with very large duration."""
        display_success_summary("Success", 9999.99, operation_type="capture")
        
        captured = capsys.readouterr()
        assert "9999.99 seconds" in captured.out


class TestOutputFormatting:
    """Test output formatting consistency."""
    
    def test_duration_formatting_precision(self, capsys):
        """Test that duration is always formatted to 2 decimal places."""
        test_cases = [
            (0, "0.00 seconds"),
            (1, "1.00 seconds"),
            (1.5, "1.50 seconds"),
            (1.234, "1.23 seconds"),
            (1.999, "2.00 seconds"),  # Should round up
        ]
        
        for duration, expected in test_cases:
            display_success_summary("Success", duration, operation_type="capture")
            captured = capsys.readouterr()
            assert expected in captured.out
    
    def test_similarity_score_formatting(self, capsys):
        """Test that similarity score is formatted correctly."""
        test_cases = [
            (0, "0.00%"),
            (0.5, "50.00%"),
            (0.999, "99.90%"),
            (1.0, "100.00%"),
            (0.12345, "12.35%"),  # Should round to 2 decimal places
        ]
        
        for score, expected in test_cases:
            display_success_summary("Success", 1.0, similarity_score=score, operation_type="compare")
            captured = capsys.readouterr()
            assert expected in captured.out
    
    def test_consistent_table_structure(self, capsys):
        """Test that all functions produce consistent table structure."""
        # Test that all summary outputs contain the same basic elements
        display_success_summary("Success", 1.0, operation_type="capture")
        captured = capsys.readouterr()
        
        # Should contain these standard table elements
        assert "Result" in captured.out
        assert "Duration" in captured.out
        assert "Success" in captured.out
        assert "1.00 seconds" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 