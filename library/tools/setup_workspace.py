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
        'description': 'Shared Resonance7 resources (includes universal tools in library/tools/)'
    },
    'sessions': {
        'type': 'symlink',
        'source': 'sessions', 
        'description': 'Shared session management'
    }
    # Note: 'tools' is no longer symlinked - projects get their own independent tools/ directory
    # Universal tools are now in library/tools/ and accessible via library/ symlink
    # Batch files are in library/ and accessible via library/ symlink
}

# Project template structure
PROJECT_TEMPLATE = {
    'src': 'Project source code',
    'docs': 'Project documentation', 
    'tests': 'Project tests',
    'tools': 'Project-specific tools (independent, not symlinked)',
    '.cursor': 'Project-specific Cursor config',
    '.gitignore': 'Project-specific gitignore',
    '.cursorignore': 'Cursor IDE ignore rules',
    '.agentignore': 'Agent file modification protection rules',
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
        for dir_name in ['src', 'docs', 'tests', 'tools']:
            (project_path / dir_name).mkdir(exist_ok=True)
            info(f"Created directory: {dir_name}/")
        
        # Note: .cursor directory is shared from root level
        info("Using shared .cursor configuration from workspace root")
        info("Created independent tools/ directory (not symlinked - for project-specific tools)")
        
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
                    # Check if it's a file or directory
                    is_file = config.get('is_file', False) or source_path.is_file()
                    mklink_flag = '' if is_file else '/D'  # No flag for files, /D for directories
                    
                    # Build mklink command
                    cmd = ['mklink']
                    if mklink_flag:
                        cmd.append(mklink_flag)
                    cmd.extend([str(target_path), str(source_path)])
                    
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
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
                        # Final fallback: copy file or directory
                        if source_path.is_dir():
                            shutil.copytree(source_path, target_path)
                            info(f"Copied directory: {resource_name} -> {target_path}")
                        else:
                            shutil.copy2(source_path, target_path)
                            info(f"Copied file: {resource_name} -> {target_path}")
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
        
        # Create .cursorignore
        cursorignore_content = """# Cursor IDE Ignore File
# Files and directories that Cursor should ignore when indexing and searching
#
# Note: Ignore patterns cascade from parent directories. To override a parent-level
# ignore pattern, use the negation operator (!). For example:
#   If D:\\Development\\Resonance7\\.cursorignore ignores "special_tools/"
#   You can re-enable it in this project with: !special_tools/

# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/
.eggs/

# Virtual environments
.env
.venv
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*.sublime-*

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs and temporary files
*.log
*.tmp
*.temp

# Database files (if applicable)
*.db
*.sqlite
*.sqlite3

# Large data files (project-specific - adjust as needed)
# *.csv
# *.json
# data/
# datasets/

# Compiled files
*.pyc
*.pyo
*.pyd
.Python

# Distribution / packaging
*.egg
wheels/
*.whl

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Project-specific exclusions
# Add project-specific patterns here

# Override parent-level ignores (if needed)
# Use ! to negate patterns from higher-level .cursorignore files
# Example: !special_tools/  (re-enables a directory ignored at parent level)
"""
        (project_path / '.cursorignore').write_text(cursorignore_content)
        info("Created .cursorignore")
        
        # Create .agentignore
        agentignore_content = """# Agent Ignore File
# Files and directories that the agent should NOT modify unless explicitly requested
# Referenced in agent_foundation.json file_safety protocol
#
# Note: Ignore patterns cascade from parent directories. To override a parent-level
# ignore pattern, use the negation operator (!). For example:
#   If D:\\Development\\Resonance7\\.agentignore ignores "special_tools/"
#   You can re-enable it in this project with: !special_tools/

# Core project configuration (protect from accidental modification)
.gitignore
.cursorignore
.agentignore
README.md
requirements.txt
pyproject.toml
setup.py
setup.cfg

# Shared Resonance 7 resources (symlinked - do not modify)
library/
sessions/
# Note: tools/ is now independent (not symlinked) - project-specific tools go here
# Universal tools are in library/tools/ and accessible via library/ symlink

# Version control
.git/
.gitattributes

# IDE configuration (usually user-specific)
.vscode/
.idea/
*.code-workspace

# Virtual environments (system-managed)
.env
.venv
venv/
env/
ENV/

# Build artifacts (regenerated, not edited)
__pycache__/
*.pyc
*.pyo
*.pyd
dist/
build/
*.egg-info/
.eggs/
wheels/
*.whl
*.egg

# Test artifacts (regenerated)
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/
.pytest_cache/

# Logs (append-only, not edited)
*.log

# Database files (data integrity - modify only with explicit request)
*.db
*.sqlite
*.sqlite3

# Large data files (protect from accidental processing)
# Uncomment and customize based on project needs:
# *.csv
# *.json
# data/
# datasets/
# *.parquet
# *.h5
# *.hdf5

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Temporary files
*.tmp
*.temp
*.bak
*.swp

# Project-specific protected files
# Add files/directories that should never be auto-modified:
# config/production.yaml
# secrets/
# credentials/

# Override parent-level ignores (if needed)
# Use ! to negate patterns from higher-level .agentignore files
# Example: !special_tools/  (re-enables a directory ignored at parent level)
"""
        (project_path / '.agentignore').write_text(agentignore_content)
        info("Created .agentignore")
        
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
        for dir_name in ['src', 'docs', 'tests', 'tools']:
            (template_dir / dir_name).mkdir(exist_ok=True)
        
        # Create directory READMEs
        src_readme = """# Source Code

This directory contains the project's source code.

## Structure

Organize your source code as appropriate for your project:
- Main application code
- Modules and packages
- Configuration files
- Resources and assets

## Best Practices

- Keep source code organized by feature or module
- Follow language-specific conventions
- Include appropriate documentation
- Maintain clear separation of concerns
"""
        (template_dir / 'src' / 'README.md').write_text(src_readme)
        
        tests_readme = """# Tests

This directory contains test files for the project.

## Structure

Organize tests to mirror your source code structure:
- Unit tests
- Integration tests
- Test fixtures and data
- Test utilities

## Best Practices

- Keep tests organized and maintainable
- Use descriptive test names
- Follow testing best practices for your language/framework
- Maintain good test coverage
"""
        (template_dir / 'tests' / 'README.md').write_text(tests_readme)
        
        tools_readme = """# Project-Specific Tools

This directory contains tools and scripts specific to this project.

## Purpose

Project-specific utilities, scripts, and helper tools that are not part of the main source code but are used for development, maintenance, or project-specific tasks.

## Universal Tools

Universal Resonance7 tools are available via the `library/` symlink:
- `library/tools/session_tools.py` - Session creation and management
- `library/tools/setup_workspace.py` - Workspace setup utility
- `library/tools/session_tools.bat` - Quick launcher for session management
- `library/tools/setup_workspace.bat` - Quick launcher for workspace setup

## Best Practices

- Keep project-specific tools organized
- Document tool usage and purpose
- Use appropriate file naming conventions
- Consider adding helper scripts for common project tasks
"""
        (template_dir / 'tools' / 'README.md').write_text(tools_readme)
        
        # Create template files
        template_readme = """# Resonance 7 Workspace Template

**Version: 1.2.0**

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
- `tools/` - Project-specific tools (independent, not symlinked)
- `.gitignore` - Git ignore rules
- `.cursorignore` - Cursor IDE ignore rules
- `.agentignore` - Agent file modification protection rules
- `README.md` - Project documentation
- `requirements.txt` - Python dependencies

## Resonance 7 Integration

This template includes symlinks to shared Resonance7 resources:
- `library/` - Shared Resonance7 resources (including universal tools in `library/tools/`)
- `sessions/` - Shared session management
- `tools/` - Project-specific tools directory (independent, not symlinked)

Universal tools accessible via `library/` symlink:
- `library/tools/session_tools.py` - Session creation and management
- `library/tools/setup_workspace.py` - Workspace setup utility
- `library/tools/session_tools.bat` - Quick launcher for session management
- `library/tools/setup_workspace.bat` - Quick launcher for workspace setup

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

# Shared Resonance 7 resources (symlinked - do not modify)
library/
sessions/
# Note: tools/ is now independent (not symlinked) - project-specific tools go here
# Universal tools are in library/tools/ and accessible via library/ symlink
"""
        (template_dir / '.gitignore').write_text(template_gitignore)
        
        # Create template .cursorignore
        template_cursorignore = """# Cursor IDE Ignore File
# Files and directories that Cursor should ignore when indexing and searching
#
# Note: Ignore patterns cascade from parent directories. To override a parent-level
# ignore pattern, use the negation operator (!). For example:
#   If D:\\Development\\Resonance7\\.cursorignore ignores "special_tools/"
#   You can re-enable it in this project with: !special_tools/

# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/
.eggs/

# Virtual environments
.env
.venv
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*.sublime-*

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs and temporary files
*.log
*.tmp
*.temp

# Database files (if applicable)
*.db
*.sqlite
*.sqlite3

# Large data files (project-specific - adjust as needed)
# *.csv
# *.json
# data/
# datasets/

# Compiled files
*.pyc
*.pyo
*.pyd
.Python

# Distribution / packaging
*.egg
wheels/
*.whl

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Project-specific exclusions
# Add project-specific patterns here

# Override parent-level ignores (if needed)
# Use ! to negate patterns from higher-level .cursorignore files
# Example: !special_tools/  (re-enables a directory ignored at parent level)
"""
        (template_dir / '.cursorignore').write_text(template_cursorignore)
        
        # Create template .agentignore
        template_agentignore = """# Agent Ignore File
# Files and directories that the agent should NOT modify unless explicitly requested
# Referenced in agent_foundation.json file_safety protocol
#
# Note: Ignore patterns cascade from parent directories. To override a parent-level
# ignore pattern, use the negation operator (!). For example:
#   If D:\\Development\\Resonance7\\.agentignore ignores "special_tools/"
#   You can re-enable it in this project with: !special_tools/

# Core project configuration (protect from accidental modification)
.gitignore
.cursorignore
.agentignore
README.md
requirements.txt
pyproject.toml
setup.py
setup.cfg

# Shared Resonance 7 resources (symlinked - do not modify)
library/
sessions/
# Note: tools/ is now independent (not symlinked) - project-specific tools go here
# Universal tools are in library/tools/ and accessible via library/ symlink

# Version control
.git/
.gitattributes

# IDE configuration (usually user-specific)
.vscode/
.idea/
*.code-workspace

# Virtual environments (system-managed)
.env
.venv
venv/
env/
ENV/

# Build artifacts (regenerated, not edited)
__pycache__/
*.pyc
*.pyo
*.pyd
dist/
build/
*.egg-info/
.eggs/
wheels/
*.whl
*.egg

# Test artifacts (regenerated)
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/
.pytest_cache/

# Logs (append-only, not edited)
*.log

# Database files (data integrity - modify only with explicit request)
*.db
*.sqlite
*.sqlite3

# Large data files (protect from accidental processing)
# Uncomment and customize based on project needs:
# *.csv
# *.json
# data/
# datasets/
# *.parquet
# *.h5
# *.hdf5

# OS files
.DS_Store
Thumbs.db
desktop.ini

# Temporary files
*.tmp
*.temp
*.bak
*.swp

# Project-specific protected files
# Add files/directories that should never be auto-modified:
# config/production.yaml
# secrets/
# credentials/

# Override parent-level ignores (if needed)
# Use ! to negate patterns from higher-level .agentignore files
# Example: !special_tools/  (re-enables a directory ignored at parent level)
"""
        (template_dir / '.agentignore').write_text(template_agentignore)
        
        # Create template requirements.txt
        template_requirements = """# Resonance 7 Workspace Template
# Add your project dependencies here

# Example:
# requests>=2.25.0
# numpy>=1.20.0
"""
        (template_dir / 'requirements.txt').write_text(template_requirements)
        
        # Restore preserved ARCHITECTURE.md if it was saved
        # (This will be set by the workflow function before calling this)
        if hasattr(create_workspace_template, '_preserved_arch'):
            arch_file = template_dir / 'docs' / 'ARCHITECTURE.md'
            arch_file.parent.mkdir(parents=True, exist_ok=True)
            arch_file.write_text(create_workspace_template._preserved_arch, encoding='utf-8')
            info("Restored ARCHITECTURE.md in template")
            delattr(create_workspace_template, '_preserved_arch')
        
        # Restore preserved directory READMEs if they were saved
        if hasattr(create_workspace_template, '_preserved_readmes'):
            for dir_name, readme_content in create_workspace_template._preserved_readmes.items():
                readme_file = template_dir / dir_name / 'README.md'
                readme_file.parent.mkdir(parents=True, exist_ok=True)
                readme_file.write_text(readme_content, encoding='utf-8')
                info(f"Restored {dir_name}/README.md in template")
            delattr(create_workspace_template, '_preserved_readmes')
        
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
    print("  - Project-specific configuration files (.gitignore, .cursorignore, .agentignore)")
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
        
        # Preserve ARCHITECTURE.md and directory READMEs before removing template
        arch_file = template_dir / 'docs' / 'ARCHITECTURE.md'
        preserved_arch = None
        if arch_file.exists():
            try:
                preserved_arch = arch_file.read_text(encoding='utf-8')
            except Exception:
                pass  # If we can't read it, that's okay
        
        # Preserve directory READMEs
        preserved_readmes = {}
        for dir_name in ['src', 'tests', 'tools']:
            readme_file = template_dir / dir_name / 'README.md'
            if readme_file.exists():
                try:
                    preserved_readmes[dir_name] = readme_file.read_text(encoding='utf-8')
                except Exception:
                    pass
        
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
    
    # Pass preserved files to the creation function
    if preserved_arch is not None:
        create_workspace_template._preserved_arch = preserved_arch
    if preserved_readmes:
        create_workspace_template._preserved_readmes = preserved_readmes
    
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
