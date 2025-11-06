#!/usr/bin/env python3
"""
Resonance 7 Workspace Setup Tool
=====================================

Creates new project workspaces with shared Resonance7 resources.
Sets up proper directory structure, symlinks, and configuration files.

Author: Resonance 7 Development Team
Version: 1.0.0
License: MIT
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# =============================================================================
# CONFIGURATION
# =============================================================================

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

# Shared resources that should be available in all workspaces
SHARED_RESOURCES = {
    '.cursor': {
        'type': 'symlink',
        'source': '.cursor',
        'description': 'Shared Cursor configuration'
    },
    'library': {
        'type': 'symlink', 
        'source': 'library',
        'description': 'Shared Resonance7 resources'
    },
    'sessions': {
        'type': 'symlink',
        'source': 'sessions', 
        'description': 'Shared session management'
    },
    'tools': {
        'type': 'symlink',
        'source': 'tools',
        'description': 'Shared development tools'
    }
}

# Project template structure
PROJECT_TEMPLATE = {
    'src': 'Project source code',
    'docs': 'Project documentation', 
    'tests': 'Project tests',
    '.cursor': 'Project-specific Cursor config',
    '.gitignore': 'Project-specific gitignore',
    'README.md': 'Project documentation',
    'requirements.txt': 'Project dependencies (placeholder)'
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def find_workspace_root() -> Path:
    """Find the Resonance7 workspace root."""
    current = Path.cwd()
    
    # Look for .cursor/rules/agent_onboarding.mdc
    while current != current.parent:
        if (current / '.cursor' / 'rules' / 'agent_onboarding.mdc').exists():
            return current
        current = current.parent
    
    # Fallback to current directory
    return Path.cwd()

def log(message: str) -> None:
    """Print a log message with timestamp and blue color."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Colors.BLUE}[{timestamp}]{Colors.NC} {message}")

def error(message: str) -> None:
    """Print an error message with red color."""
    print(f"{Colors.RED}ERROR:{Colors.NC} {message}", file=sys.stderr)

def success(message: str) -> None:
    """Print a success message with green color."""
    print(f"{Colors.GREEN}SUCCESS:{Colors.NC} {message}")

def warning(message: str) -> None:
    """Print a warning message with yellow color."""
    print(f"{Colors.YELLOW}WARNING:{Colors.NC} {message}")

def info(message: str) -> None:
    """Print an info message."""
    print(f"INFO: {message}")

def show_section_header(title):
    """
    Display a section header.
    
    Args:
        title (str): Section title
    
    Example output:
        -----------------------------------------------------------------
          TITLE
        -----------------------------------------------------------------
    """
    print()
    print("-" * 64)
    print(f"  {title.upper()}")
    print("-" * 64)
    print()

# =============================================================================
# WORKSPACE SETUP FUNCTIONS
# =============================================================================

def create_project_structure(project_path: Path, project_name: str) -> bool:
    """Create the basic project directory structure."""
    try:
        # Create main project directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        for dir_name in ['src', 'docs', 'tests']:
            (project_path / dir_name).mkdir(exist_ok=True)
            info(f"Created directory: {dir_name}/")
        
        # Note: .cursor directory is shared from root level
        info("Using shared .cursor configuration from workspace root")
        
        return True
        
    except Exception as e:
        error(f"Failed to create project structure: {e}")
        return False

def create_symlinks(project_path: Path, workspace_root: Path) -> bool:
    """Create symlinks to shared resources."""
    try:
        for resource_name, config in SHARED_RESOURCES.items():
            source_path = workspace_root / config['source']
            target_path = project_path / resource_name
            
            if not source_path.exists():
                warning(f"Source path does not exist: {source_path}")
                continue
                
            if target_path.exists():
                if target_path.is_symlink():
                    info(f"Symlink already exists: {resource_name}")
                    continue
                else:
                    warning(f"Path exists but is not a symlink: {resource_name}")
                    continue
            
            try:
                # Try symbolic link first (shows shortcut arrow on Windows)
                if sys.platform == "win32":
                    import subprocess
                    # Use mklink /D for directory symbolic links, suppress output
                    result = subprocess.run([
                        'mklink', '/D', str(target_path), str(source_path)
                    ], shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        info(f"Created symbolic link: {resource_name} -> {source_path}")
                    else:
                        raise subprocess.CalledProcessError(result.returncode, 'mklink')
                else:
                    # Unix-style symlink
                    relative_source = os.path.relpath(source_path, project_path)
                    target_path.symlink_to(relative_source)
                    info(f"Created symlink: {resource_name} -> {relative_source}")
            except (OSError, subprocess.CalledProcessError):
                # Fallback: try directory junction (Windows) or copy
                if sys.platform == "win32":
                    try:
                        # Try directory junction as fallback, suppress output
                        import subprocess
                        result = subprocess.run([
                            'mklink', '/J', str(target_path), str(source_path)
                        ], shell=True, capture_output=True, text=True)
                        if result.returncode == 0:
                            info(f"Created directory junction: {resource_name} -> {source_path}")
                        else:
                            raise subprocess.CalledProcessError(result.returncode, 'mklink')
                    except subprocess.CalledProcessError:
                        # Final fallback: copy directory
                        if source_path.is_dir():
                            shutil.copytree(source_path, target_path)
                        else:
                            shutil.copy2(source_path, target_path)
                        info(f"Copied directory: {resource_name} -> {target_path}")
                else:
                    error(f"Failed to create symlink {resource_name}")
                    error(f"Manual fix: Run 'ln -s {source_path} {target_path}'")
                    return False
        
        return True
        
    except Exception as e:
        error(f"Failed to create symlinks: {e}")
        return False

def create_project_files(project_path: Path, project_name: str) -> bool:
    """Create project-specific files."""
    try:
        # Create .gitignore
        gitignore_content = f"""# {project_name} - Project-specific gitignore
# Generated by Resonance 7 Workspace Setup

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.tmp
"""
        (project_path / '.gitignore').write_text(gitignore_content)
        info("Created .gitignore")
        
        # Create README.md
        readme_content = f"""# {project_name}

Project description goes here.

## Getting Started

1. Set up virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the project:
   ```bash
   python src/main.py
   ```

## Project Structure

- `src/` - Source code
- `docs/` - Documentation
- `tests/` - Test files
- `requirements.txt` - Python dependencies

## Development

This project follows the Resonance7 development standards.
The `.cursor` configuration is shared from the workspace root level.
"""
        (project_path / 'README.md').write_text(readme_content)
        info("Created README.md")
        
        # Create requirements.txt placeholder
        requirements_content = f"""# {project_name} Dependencies
# Add your project dependencies here

# Example:
# requests>=2.25.0
# numpy>=1.20.0
"""
        (project_path / 'requirements.txt').write_text(requirements_content)
        info("Created requirements.txt")
        
        # Note: .cursor settings are inherited from workspace root
        info("Using shared .cursor settings from workspace root")
        
        return True
        
    except Exception as e:
        error(f"Failed to create project files: {e}")
        return False

def create_workspace_template(workspace_root: Path) -> bool:
    """Create the workspace template directory."""
    try:
        template_dir = workspace_root / 'library' / 'workspace_template'
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Create template structure
        for dir_name in ['src', 'docs', 'tests']:
            (template_dir / dir_name).mkdir(exist_ok=True)
        
        # Create template files
        template_readme = """# Resonance 7 Workspace Template

This template provides the standard structure for new Resonance7 projects.

## Usage

1. Copy this template to create a new project
2. Rename the directory to your project name
3. Update the README.md and requirements.txt files
4. Start developing!

## Structure

- `src/` - Source code
- `docs/` - Documentation  
- `tests/` - Test files
- `.gitignore` - Git ignore rules
- `README.md` - Project documentation
- `requirements.txt` - Python dependencies

## Resonance 7 Integration

This template includes symlinks to shared Resonance7 resources:
- `library/` - Shared Resonance7 resources (including this template)
- `sessions/` - Shared session management
- `tools/` - Shared development tools

The `.cursor` configuration is shared from the workspace root level.

## Location

This template is stored in `library/workspace_template/` and serves as the master blueprint for all new Resonance7 projects.
"""
        (template_dir / 'README.md').write_text(template_readme)
        
        # Create template .gitignore
        template_gitignore = """# Resonance 7 Workspace Template
# Copy this to your project and customize as needed

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.tmp
"""
        (template_dir / '.gitignore').write_text(template_gitignore)
        
        # Create template requirements.txt
        template_requirements = """# Resonance 7 Workspace Template
# Add your project dependencies here

# Example:
# requests>=2.25.0
# numpy>=1.20.0
"""
        (template_dir / 'requirements.txt').write_text(template_requirements)
        
        info("Created workspace template")
        return True
        
    except Exception as e:
        error(f"Failed to create workspace template: {e}")
        return False

# =============================================================================
# MAIN WORKFLOW FUNCTIONS
# =============================================================================

def setup_new_project(project_name: str, dry_run: bool = False) -> int:
    """Set up a new project workspace."""
    workspace_root = find_workspace_root()
    projects_dir = workspace_root / 'projects'
    project_path = projects_dir / project_name
    
    show_section_header("Project Setup")
    print(f"Project: {project_name}")
    print(f"Workspace root: {workspace_root}")
    print(f"Project path: {project_path}")
    print()
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
        return 0
    
    # Create projects directory if it doesn't exist
    projects_dir.mkdir(exist_ok=True)
    
    # Check if project already exists
    if project_path.exists():
        error(f"Project '{project_name}' already exists at {project_path}")
        print()
        overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite not in ['y', 'yes']:
            info("Operation cancelled")
            return 1
        
        # Remove existing project
        try:
            if project_path.is_symlink() or project_path.is_file():
                project_path.unlink()
            else:
                shutil.rmtree(project_path)
            info(f"Removed existing project: {project_name}")
        except Exception as e:
            error(f"Failed to remove existing project: {e}")
            return 1
    
    # Create project structure
    if not create_project_structure(project_path, project_name):
        return 1
    
    # Create symlinks to shared resources
    if not create_symlinks(project_path, workspace_root):
        return 1
    
    # Create project files
    if not create_project_files(project_path, project_name):
        return 1
    
    show_section_header("Project Created")
    print(f"✅ Created: {project_path}")
    print()
    print("The project includes:")
    print("  - Complete directory structure (src/, docs/, tests/)")
    print("  - Symlinks to shared Resonance7 resources")
    print("  - Project-specific configuration files")
    print("  - Ready for development")
    print()
    
    return 0

def create_workspace_template_workflow(dry_run: bool = False) -> int:
    """Create the workspace template."""
    workspace_root = find_workspace_root()
    template_dir = workspace_root / 'library' / 'workspace_template'
    
    show_section_header("Template Creation")
    print(f"Workspace root: {workspace_root}")
    print(f"Template location: {template_dir}")
    print()
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
        return 0
    
    # Check if template already exists
    if template_dir.exists():
        warning(f"Workspace template already exists at {template_dir}")
        print()
        overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite not in ['y', 'yes']:
            info("Operation cancelled")
            return 1
        
        # Remove existing template
        try:
            if template_dir.is_symlink() or template_dir.is_file():
                template_dir.unlink()
            else:
                shutil.rmtree(template_dir)
            info("Removed existing workspace template")
        except Exception as e:
            error(f"Failed to remove existing template: {e}")
            return 1
    
    if not create_workspace_template(workspace_root):
        return 1
    
    show_section_header("Template Created")
    print("✅ Created: library/workspace_template/")
    print()
    print("The template includes:")
    print("  - Standard project structure")
    print("  - Template configuration files")
    print("  - Ready for copying to new projects")
    print()
    
    return 0

def show_main_menu() -> int:
    """Display the main menu and get user choice."""
    print("-" * 64)
    print("  WORKSPACE SETUP")
    print("-" * 64)
    print()
    print("What would you like to do?")
    print()
    print("1. Create new project workspace")
    print("2. Create workspace template")
    print("3. Show workspace structure")
    print("4. Cancel")
    print()
    
    while True:
        choice = input("Choice [1-4]: ").strip()
        if choice in ['1', '2', '3', '4']:
            return int(choice)
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def show_workspace_structure() -> None:
    """Display the current workspace structure."""
    workspace_root = find_workspace_root()
    
    print("=" * 64)
    print("  WORKSPACE STRUCTURE")
    print("=" * 64)
    print()
    print(f"Workspace Root: {workspace_root}")
    print()
    
    # Show shared resources
    print("Shared Resources:")
    for resource_name, config in SHARED_RESOURCES.items():
        source_path = workspace_root / config['source']
        status = "✓" if source_path.exists() else "✗"
        print(f"  {status} {resource_name} -> {config['source']} ({config['description']})")
    
    print()
    
    # Show projects directory
    projects_dir = workspace_root / 'projects'
    if projects_dir.exists():
        print("Projects:")
        for project in projects_dir.iterdir():
            if project.is_dir():
                print(f"  📁 {project.name}")
    else:
        print("Projects: (none created yet)")
    
    print()
    
    # Show template
    template_dir = workspace_root / 'library' / 'workspace_template'
    if template_dir.exists():
        print("Template: ✓ library/workspace_template/")
    else:
        print("Template: ✗ (not created yet)")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Resonance 7 Workspace Setup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_workspace.py                    # Interactive mode
  python setup_workspace.py --project my-app  # Create project directly
  python setup_workspace.py --template        # Create template only
  python setup_workspace.py --dry-run         # Preview changes
        """
    )
    
    parser.add_argument(
        '--project', 
        type=str, 
        help='Name of project to create (skips interactive mode)'
    )
    parser.add_argument(
        '--template', 
        action='store_true', 
        help='Create workspace template only'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Preview changes without making them'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='Resonance 7 Workspace Setup 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle direct project creation
    if args.project:
        return setup_new_project(args.project, args.dry_run)
    
    # Handle template creation
    if args.template:
        return create_workspace_template_workflow(args.dry_run)
    
    # Show header
    workspace_root = find_workspace_root()
    print("=" * 64)
    print("  Resonance 7 - Workspace Setup Tool")
    print("=" * 64)
    print()
    print(f"Workspace Root: {workspace_root}")
    print()
    
    # Dry run notice
    if args.dry_run:
        print("DRY RUN MODE - No files will be created or modified")
        print()
    
    # Interactive mode
    while True:
        choice = show_main_menu()
        
        if choice == 1:
            # Create new project
            project_name = input("\nEnter project name: ").strip()
            if not project_name:
                error("Project name is required")
                continue
            
            if setup_new_project(project_name, args.dry_run) == 0:
                break
                
        elif choice == 2:
            # Create template
            if create_workspace_template_workflow(args.dry_run) == 0:
                break
                
        elif choice == 3:
            # Show structure
            show_workspace_structure()
            input("\nPress Enter to continue...")
            
        elif choice == 4:
            # Cancel
            print("\nGoodbye!")
            break
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
