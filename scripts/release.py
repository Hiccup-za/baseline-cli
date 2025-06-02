#!/usr/bin/env python3
"""
Release helper script for baseline-cli

This script helps automate the release process by:
1. Updating the version in __version__.py
2. Checking that CHANGELOG.md has an entry for the new version
3. Creating and pushing a git tag to trigger the release workflow

Usage:
    python scripts/release.py 0.1.3          # Create release v0.1.3
    python scripts/release.py 0.1.3 --dry-run  # Preview what would happen
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

# Rich imports for beautiful output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import print as rich_print
    console = Console()
except ImportError:
    print("⚠️  Rich not available, using basic output")
    console = None
    rich_print = print

def run_command(cmd, check=True, capture=True):
    """Run a shell command and return the result"""
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, check=check, 
                                  capture_output=True, text=True)
            return result.stdout.strip()
        else:
            result = subprocess.run(cmd, shell=True, check=check)
            return result.returncode == 0
    except subprocess.CalledProcessError as e:
        if console:
            console.print(f"[red]❌ Command failed: {cmd}[/red]")
            console.print(f"[red]Error: {e.stderr}[/red]")
        else:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {e.stderr}")
        return None

def validate_version(version):
    """Validate that version follows semantic versioning"""
    pattern = r'^\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?$'
    if not re.match(pattern, version):
        return False, "Version must follow semantic versioning (e.g., 1.0.0, 1.0.0-beta)"
    return True, ""

def get_current_version():
    """Get the current version from __version__.py"""
    try:
        with open('__version__.py', 'r') as f:
            content = f.read()
        
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
        else:
            return None
    except FileNotFoundError:
        return None

def update_version_file(new_version):
    """Update the version in __version__.py"""
    try:
        with open('__version__.py', 'r') as f:
            content = f.read()
        
        # Replace the version string
        updated_content = re.sub(
            r'(__version__\s*=\s*["\'])[^"\']+(["\'])',
            rf'\g<1>{new_version}\g<2>',
            content
        )
        
        with open('__version__.py', 'w') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        if console:
            console.print(f"[red]❌ Failed to update __version__.py: {e}[/red]")
        else:
            print(f"❌ Failed to update __version__.py: {e}")
        return False

def check_changelog(version):
    """Check if CHANGELOG.md has an entry for this version"""
    try:
        with open('CHANGELOG.md', 'r') as f:
            content = f.read()
        
        # Look for version entry
        pattern = rf'## \[{re.escape(version)}\]'
        if re.search(pattern, content):
            return True, "Found changelog entry"
        else:
            return False, f"No changelog entry found for version {version}"
    except FileNotFoundError:
        return False, "CHANGELOG.md not found"

def check_git_status():
    """Check if git working directory is clean"""
    status = run_command("git status --porcelain")
    if status is None:
        return False, "Failed to check git status"
    
    if status:
        return False, "Working directory has uncommitted changes"
    else:
        return True, "Working directory is clean"

def create_and_push_tag(version, dry_run=False):
    """Create and push a git tag"""
    tag = f"v{version}"
    
    if dry_run:
        if console:
            console.print(f"[yellow]🏷️  Would create tag: {tag}[/yellow]")
            console.print(f"[yellow]📤 Would push tag to origin[/yellow]")
        else:
            print(f"🏷️  Would create tag: {tag}")
            print("📤 Would push tag to origin")
        return True
    
    # Create the tag
    commit_msg = f"Release v{version}"
    if not run_command(f'git tag -a {tag} -m "{commit_msg}"', capture=False):
        return False
    
    # Push the tag
    if not run_command(f"git push origin {tag}", capture=False):
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Create a new release of baseline-cli")
    parser.add_argument("version", help="Version number (e.g., 0.1.3)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Preview what would happen without making changes")
    
    args = parser.parse_args()
    
    # Change to repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    if console:
        console.print(Panel.fit(f"🚀 [bold]baseline-cli Release Helper[/bold]", 
                               style="blue"))
    else:
        print("🚀 baseline-cli Release Helper")
        print("=" * 50)
    
    # Validate version format
    valid, error = validate_version(args.version)
    if not valid:
        if console:
            console.print(f"[red]❌ Invalid version format: {error}[/red]")
        else:
            print(f"❌ Invalid version format: {error}")
        sys.exit(1)
    
    # Get current version
    current_version = get_current_version()
    if not current_version:
        if console:
            console.print("[red]❌ Could not read current version from __version__.py[/red]")
        else:
            print("❌ Could not read current version from __version__.py")
        sys.exit(1)
    
    # Create summary table
    if console:
        table = Table(show_header=False, box=None)
        table.add_row("Current Version", current_version)
        table.add_row("New Version", args.version)
        table.add_row("Mode", "DRY RUN" if args.dry_run else "LIVE")
        console.print()
        console.print(table)
        console.print()
    else:
        print(f"Current Version: {current_version}")
        print(f"New Version: {args.version}")
        print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
        print()
    
    # Pre-flight checks
    checks = []
    
    # Check git status
    clean, status_msg = check_git_status()
    checks.append(("Git Status", "✅" if clean else "❌", status_msg))
    
    # Check changelog
    has_changelog, changelog_msg = check_changelog(args.version)
    checks.append(("Changelog", "✅" if has_changelog else "⚠️", changelog_msg))
    
    # Display checks
    if console:
        console.print("[bold]Pre-flight Checks:[/bold]")
        for check_name, status, message in checks:
            console.print(f"{status} {check_name}: {message}")
        console.print()
    else:
        print("Pre-flight Checks:")
        for check_name, status, message in checks:
            print(f"{status} {check_name}: {message}")
        print()
    
    # Stop if critical checks fail
    if not clean:
        if console:
            console.print("[red]❌ Cannot proceed with uncommitted changes[/red]")
        else:
            print("❌ Cannot proceed with uncommitted changes")
        sys.exit(1)
    
    if not has_changelog:
        if console:
            console.print("[yellow]⚠️  No changelog entry found. Consider updating CHANGELOG.md[/yellow]")
        else:
            print("⚠️  No changelog entry found. Consider updating CHANGELOG.md")
    
    # Update version file
    version_needs_update = current_version != args.version
    
    if args.dry_run:
        if version_needs_update:
            if console:
                console.print(f"[yellow]📝 Would update __version__.py from {current_version} to {args.version}[/yellow]")
            else:
                print(f"📝 Would update __version__.py from {current_version} to {args.version}")
        else:
            if console:
                console.print(f"[yellow]📝 Version is already {args.version}, no update needed[/yellow]")
            else:
                print(f"📝 Version is already {args.version}, no update needed")
    else:
        if version_needs_update:
            if update_version_file(args.version):
                if console:
                    console.print(f"[green]✅ Updated __version__.py from {current_version} to {args.version}[/green]")
                else:
                    print(f"✅ Updated __version__.py from {current_version} to {args.version}")
            else:
                sys.exit(1)
        else:
            if console:
                console.print(f"[green]✅ Version is already {args.version}, no update needed[/green]")
            else:
                print(f"✅ Version is already {args.version}, no update needed")
    
    # Commit the version change (only if there was an update)
    if not args.dry_run and version_needs_update:
        commit_msg = f"Bump version to {args.version}"
        if not run_command(f'git add __version__.py && git commit -m "{commit_msg}"', capture=False):
            if console:
                console.print("[red]❌ Failed to commit version change[/red]")
            else:
                print("❌ Failed to commit version change")
            sys.exit(1)
        
        if console:
            console.print("[green]✅ Committed version change[/green]")
        else:
            print("✅ Committed version change")
    elif not args.dry_run:
        if console:
            console.print("[green]✅ No version change to commit[/green]")
        else:
            print("✅ No version change to commit")
    
    # Create and push tag
    if create_and_push_tag(args.version, args.dry_run):
        if console:
            console.print(f"[green]✅ {'Would create and push' if args.dry_run else 'Created and pushed'} tag v{args.version}[/green]")
        else:
            print(f"✅ {'Would create and push' if args.dry_run else 'Created and pushed'} tag v{args.version}")
    else:
        if console:
            console.print("[red]❌ Failed to create/push tag[/red]")
        else:
            print("❌ Failed to create/push tag")
        sys.exit(1)
    
    # Final instructions
    if console:
        console.print()
        if args.dry_run:
            console.print(Panel.fit(
                "[bold green]✅ Dry run completed successfully![/bold green]\n"
                f"Run without --dry-run to create release v{args.version}",
                style="green"
            ))
        else:
            console.print(Panel.fit(
                f"[bold green]🎉 Release v{args.version} initiated![/bold green]\n"
                "Check GitHub Actions for release workflow progress:\n"
                "https://github.com/your-username/baseline-cli/actions",
                style="green"
            ))
    else:
        print()
        if args.dry_run:
            print("✅ Dry run completed successfully!")
            print(f"Run without --dry-run to create release v{args.version}")
        else:
            print(f"🎉 Release v{args.version} initiated!")
            print("Check GitHub Actions for release workflow progress")

if __name__ == "__main__":
    main() 