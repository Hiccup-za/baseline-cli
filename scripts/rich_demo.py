from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

# Simulate steps (in a real script, these would be your actual steps)
console.print()  # Blank line before steps
console.print("[dim]Visiting URL...[/dim]")
console.print("[dim]Screenshot captured[/dim]")
console.print("[dim]Results compiled[/dim]")

# Stylish summary table
result = "Success"
duration = 3.30

# Table with colored headers and values
table = Table(show_header=False, box=None, pad_edge=False)
table.add_row("📊 [bold cyan]Result[/bold cyan]", "[green]Success[/green]")
table.add_row("⏱️  [bold cyan]Duration[/bold cyan]", f"[white]{duration:.2f} seconds[/white]")

panel_title = Text("Baseline Capture Summary", style="bold blue")
console.print(Panel(table, title=panel_title, border_style="cyan", box=box.ROUNDED, expand=False)) 