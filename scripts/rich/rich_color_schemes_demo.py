from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
import time

console = Console()

result = "Success"
duration = 3.30

# 1. Classic Blue & White
panel_title1 = Text("Baseline Capture Summary", style="bold blue")
table1 = Table(show_header=False, box=None, pad_edge=False)
table1.add_row("📊 [bold cyan]Result[/bold cyan]", "[green]Success[/green]")
table1.add_row("⏱️  [bold cyan]Duration[/bold cyan]", f"[white]{duration:.2f} seconds[/white]")

console.print("\n[bold]Classic Blue & White:[/bold]")
console.print(Panel(table1, title=panel_title1, border_style="cyan", box=box.ROUNDED, expand=False))

# Pause before next scheme
time.sleep(1.5)
console.print("\n[dim]--- Switching to Dracula (Purple & Pink) ---[/dim]\n")
time.sleep(1)

# 2. Dracula (Purple & Pink)
panel_title2 = Text("Baseline Capture Summary", style="bold magenta")
table2 = Table(show_header=False, box=None, pad_edge=False)
table2.add_row("🦇 [bold magenta]Result[/bold magenta]", "[bright_green]Success[/bright_green]")
table2.add_row("⏱️  [bold magenta]Duration[/bold magenta]", f"[white]{duration:.2f} seconds[/white]")

console.print("[bold]Dracula (Purple & Pink):[/bold]")
console.print(Panel(table2, title=panel_title2, border_style="magenta", box=box.ROUNDED, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Monochrome Gray ---[/dim]\n")
time.sleep(1)

# 3. Monochrome Gray
panel_title3 = Text("Baseline Capture Summary", style="bold bright_black")
table3 = Table(show_header=False, box=None, pad_edge=False)
table3.add_row("⬜ [bold gray70]Result[/bold gray70]", "[white]Success[/white]")
table3.add_row("⏱️  [bold gray70]Duration[/bold gray70]", f"[white]{duration:.2f} seconds[/white]")

console.print("[bold]Monochrome Gray:[/bold]")
console.print(Panel(table3, title=panel_title3, border_style="gray50", box=box.ROUNDED, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Solarized ---[/dim]\n")
time.sleep(1)

# 4. Solarized
panel_title4 = Text("Baseline Capture Summary", style="bold bright_yellow")
table4 = Table(show_header=False, box=None, pad_edge=False)
table4.add_row("🌞 [bold bright_cyan]Result[/bold bright_cyan]", "[bright_green]Success[/bright_green]")
table4.add_row("⏱️  [bold bright_cyan]Duration[/bold bright_cyan]", f"[bright_white]{duration:.2f} seconds[/bright_white]")

console.print("[bold]Solarized:[/bold]")
console.print(Panel(table4, title=panel_title4, border_style="yellow", box=box.ROUNDED, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Nord Theme (Cool Blues) ---[/dim]\n")
time.sleep(1)

# 5. Nord Theme (Cool Blues)
panel_title5 = Text("Baseline Capture Summary", style="bold bright_cyan")
table5 = Table(show_header=False, box=None, pad_edge=False)
table5.add_row("❄️ [bold bright_cyan]Result[/bold bright_cyan]", "[bright_white]Success[/bright_white]")
table5.add_row("⏱️  [bold bright_cyan]Duration[/bold bright_cyan]", f"[bright_white]{duration:.2f} seconds[/bright_white]")

console.print("[bold]Nord Theme (Cool Blues):[/bold]")
console.print(Panel(table5, title=panel_title5, border_style="bright_cyan", box=box.ROUNDED, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to High Contrast ---[/dim]\n")
time.sleep(1)

# 6. High Contrast
panel_title6 = Text("Baseline Capture Summary", style="bold white")
table6 = Table(show_header=False, box=None, pad_edge=False)
table6.add_row("⚡ [bold white]Result[/bold white]", "[green]Success[/green]")
table6.add_row("⏱️  [bold white]Duration[/bold white]", f"[yellow]{duration:.2f} seconds[/yellow]")

console.print("[bold]High Contrast:[/bold]")
console.print(Panel(table6, title=panel_title6, border_style="white", box=box.ROUNDED, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Radical Rainbow ---[/dim]\n")
time.sleep(1)

# 7. Radical Rainbow
panel_title7 = Text("Baseline Capture Summary", style="bold red")
table7 = Table(show_header=False, box=None, pad_edge=False)
table7.add_row("🌈 [bold red]Result[/bold red]", "[bold yellow]S[/bold yellow][bold green]u[/bold green][bold cyan]c[/bold cyan][bold blue]c[/bold blue][bold magenta]e[/bold magenta][bold red]s[/bold red][bold yellow]s[/bold yellow]")
table7.add_row("⏱️  [bold magenta]Duration[/bold magenta]", f"[bold blue]{duration:.2f} seconds[/bold blue]")

console.print("[bold]Radical Rainbow:[/bold]")
console.print(Panel(table7, title=panel_title7, border_style="bright_yellow", box=box.HEAVY, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Vaporwave ---[/dim]\n")
time.sleep(1)

# 8. Vaporwave
panel_title8 = Text("Baseline Capture Summary", style="bold bright_magenta")
table8 = Table(show_header=False, box=None, pad_edge=False)
table8.add_row("🦄 [bold bright_magenta]Result[/bold bright_magenta]", "[bold bright_cyan]Success[/bold bright_cyan]")
table8.add_row("⏱️  [bold bright_magenta]Duration[/bold bright_magenta]", f"[bold bright_pink]{duration:.2f} seconds[/bold bright_pink]")

console.print("[bold]Vaporwave:[/bold]")
console.print(Panel(table8, title=panel_title8, border_style="bright_cyan", box=box.DOUBLE, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Hacker Green ---[/dim]\n")
time.sleep(1)

# 9. Hacker Green
panel_title9 = Text("Baseline Capture Summary", style="bold green")
table9 = Table(show_header=False, box=None, pad_edge=False)
table9.add_row("💾 [bold green]Result[/bold green]", "[bold bright_green]Success[/bold bright_green]")
table9.add_row("⏱️  [bold green]Duration[/bold green]", f"[bold bright_green]{duration:.2f} seconds[/bold bright_green]")

console.print("[bold]Hacker Green:[/bold]")
console.print(Panel(table9, title=panel_title9, border_style="green", box=box.MINIMAL_DOUBLE_HEAD, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Firestorm ---[/dim]\n")
time.sleep(1)

# 10. Firestorm
panel_title10 = Text("Baseline Capture Summary", style="bold bright_red")
table10 = Table(show_header=False, box=None, pad_edge=False)
table10.add_row("🔥 [bold bright_red]Result[/bold bright_red]", "[bold yellow]Success[/bold yellow]")
table10.add_row("⏱️  [bold bright_red]Duration[/bold bright_red]", f"[bold yellow]{duration:.2f} seconds[/bold yellow]")

console.print("[bold]Firestorm:[/bold]")
console.print(Panel(table10, title=panel_title10, border_style="bright_red", box=box.SQUARE, expand=False))

time.sleep(1.5)
console.print("\n[dim]--- Switching to Cyberpunk ---[/dim]\n")
time.sleep(1)

# 11. Cyberpunk
panel_title11 = Text("Baseline Capture Summary", style="bold bright_magenta")
table11 = Table(show_header=False, box=None, pad_edge=False)
table11.add_row("🤖 [bold bright_magenta]Result[/bold bright_magenta]", "[bold bright_yellow]Success[/bold bright_yellow]")
table11.add_row("⏱️  [bold bright_magenta]Duration[/bold bright_magenta]", f"[bold bright_cyan]{duration:.2f} seconds[/bold bright_cyan]")

console.print("[bold]Cyberpunk:[/bold]")
console.print(Panel(table11, title=panel_title11, border_style="bright_magenta", box=box.ROUNDED, expand=False)) 