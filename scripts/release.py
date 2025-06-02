#!/usr/bin/env python3
"""
Release helper script for baseline-cli

This script helps prepare releases by:
1. Updating the version in __version__.py
2. Checking that CHANGELOG.md has an entry for the new version  
3. Committing the version change
4. Optionally creating and pushing a git tag (automated workflow handles this too)

The automated GitHub workflow will trigger when __version__.py changes on main.

Usage:
    python scripts/release.py 0.2.0          # Prepare release v0.2.0
    python scripts/release.py 0.2.0 --dry-run  # Preview what would happen
    python scripts/release.py 0.2.0 --commit-only  # Just update version and commit (recommended)
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

def commit_version_change(version, dry_run=False):
    """Commit the version change"""
    if dry_run:
        if console:
            console.print(f"[yellow]📝 Would commit version change to {version}[/yellow]")
        else:
            print(f"📝 Would commit version change to {version}")
        return True
    
    commit_msg = f"Bump version to {version}"
    if not run_command(f'git add __version__.py && git commit -m "{commit_msg}"', capture=False):
        return False
    
    return True

def create_and_push_tag(version, dry_run=False):
    """Create and push a git tag (optional with automated workflow)"""
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
    parser = argparse.ArgumentParser(description="Prepare a new release of baseline-cli")
    parser.add_argument("version", help="Version number (e.g., 0.2.0)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Preview what would happen without making changes")
    parser.add_argument("--commit-only", action="store_true",
                       help="Only update version and commit (recommended - let GitHub Actions handle the rest)")
    
    args = parser.parse_args()
    
    # Change to repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    if console:
        mode = "DRY RUN" if args.dry_run else ("COMMIT ONLY" if args.commit_only else "FULL RELEASE")
        console.print(Panel.fit(f"🚀 [bold]baseline-cli Release Helper[/bold]", 
                               style="blue"))
    else:
        mode = "DRY RUN" if args.dry_run else ("COMMIT ONLY" if args.commit_only else "FULL RELEASE")
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
        table.add_row("Mode", mode)
        console.print()
        console.print(table)
        console.print()
    else:
        print(f"Current Version: {current_version}")
        print(f"New Version: {args.version}")
        print(f"Mode: {mode}")
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
    if args.dry_run:
        if console:
            console.print(f"[yellow]📝 Would update __version__.py to {args.version}[/yellow]")
        else:
            print(f"📝 Would update __version__.py to {args.version}")
    else:
        if update_version_file(args.version):
            if console:
                console.print(f"[green]✅ Updated __version__.py to {args.version}[/green]")
            else:
                print(f"✅ Updated __version__.py to {args.version}")
        else:
            sys.exit(1)
    
    # Commit the version change
    if commit_version_change(args.version, args.dry_run):
        if console:
            console.print(f"[green]✅ {'Would commit' if args.dry_run else 'Committed'} version change[/green]")
        else:
            print(f"✅ {'Would commit' if args.dry_run else 'Committed'} version change")
    else:
        if console:
            console.print("[red]❌ Failed to commit version change[/red]")
        else:
            print("❌ Failed to commit version change")
        sys.exit(1)
    
    # Handle tagging (optional in automated workflow)
    if not args.commit_only:
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
                f"Run without --dry-run to prepare release v{args.version}",
                style="green"
            ))
        elif args.commit_only:
            console.print(Panel.fit(
                f"[bold green]🎉 Release v{args.version} prepared![/bold green]\n"
                "Push to main branch and GitHub Actions will automatically:\n"
                "• Create the git tag\n"
                "• Create the GitHub Release\n" 
                "• Extract changelog content\n"
                "• Upload release assets",
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
            print(f"Run without --dry-run to prepare release v{args.version}")
        elif args.commit_only:
            print(f"🎉 Release v{args.version} prepared!")
            print("Push to main and GitHub Actions will handle the rest")
        else:
            print(f"🎉 Release v{args.version} initiated!")
            print("Check GitHub Actions for release workflow progress")

if __name__ == "__main__":
    main() 