#!/usr/bin/env python3
"""
Resonance 7 Project Setup Tool
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
# PROJECT SETUP FUNCTIONS
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
        # Note: .gitignore, .cursorignore, and .agentignore are handled at workspace root level.
        # Add project-specific versions only if needed (e.g., when project has its own Git repo).
        
        # Create README.md (with integrated development log)
        readme_content = f"""# {project_name}

[Brief project description - one to three sentences explaining what this project does and its primary purpose.]

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Development Status](#development-status)
- [Development Log](#development-log)
- [Related Sessions](#related-sessions)

---

## Features

- [Feature 1] - [Brief description]
- [Feature 2] - [Brief description]
- [Feature 3] - [Brief description]

---

## Getting Started

### Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]

### Installation

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

### Quick Start

```bash
# Example command
[command here]
```

---

## Project Structure

```
{project_name}/
├── src/                    # Source code
├── tests/                  # Test files
├── tools/                  # Project-specific tools
├── README.md               # This file
├── requirements.txt        # Python dependencies
│
├── library/                # Symlink → Shared Resonance7 resources
├── sessions/               # Symlink → Shared session management
└── .cursor/                # Symlink → Shared Cursor configuration
```

---

## Usage

[How to use the project - examples, commands, API overview, etc.]

```bash
# Example usage
[example command]
```

---

## Development Status

**Current State**: [Brief status - Working/Broken/In Progress]

**Last Updated**: [YYYY-MM-DD]

**Build Status**: [Success/Failure/Not Tested]

**Known Issues**:
- [Issue 1] - [Brief description]
- [Issue 2] - [Brief description]

---

## Development Log

> **Note**: This log tracks project-wide progress across all sessions. For detailed session-by-session work, see `sessions/current/`.

### Summary

[Main accomplishments, decisions, and key insights across all sessions.]

### Key Decisions & Rationale

- **Decision 1** – [Brief reasoning]
- **Decision 2** – [Brief reasoning]

### Recent Work

#### [YYYY-MM-DD] - [Session ID: YYYYMMDD-NN]
- [What was done in this session]
- [Key changes or additions]
- [Files created/modified]

#### [Previous Session]
- [Previous session work]

### Deliverables & Metrics

- ✅ **Deliverable 1** – [File / feature] — [LoC / size / metric]
- 🚧 **Partial Deliverable** – [Status % or remaining tasks]
- 📊 **Metric** – [Coverage %, build time, etc.]

### Implementation Highlights

- [Notable techniques, libraries, commands, patterns]
- [Key architectural decisions]

### Challenges, Failures & Lessons

#### **Problem [N]: [Brief description]**
- **Issue**: [What went wrong]
- **Root Cause**: [Why it happened]
- **Solution / Work-around**: [How it was fixed]
- **Lesson**: [One-line takeaway]

### Next Work Items

**High Priority**:
- [Task 1]
- [Task 2]

**Medium Priority**:
- [Task 1]
- [Task 2]

**Low Priority**:
- [Task 1]
- [Task 2]

---

## Related Sessions

Session logs documenting work on this project:

- **[YYYYMMDD-NN](sessions/current/YYYYMMDD-NN.md)** – [Brief description of work done]
- **[YYYYMMDD-NN](sessions/current/YYYYMMDD-NN.md)** – [Brief description of work done]
- **[YYYYMMDD-NN](sessions/recent/YYYYMMDD-NN.md)** – [Brief description of work done]

> **Note**: Session logs are automatically archived after 7 days. Older sessions can be found in `sessions/recent/` or `sessions/archived/`.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
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
        
        # Create directory READMEs (minimal placeholders)
        src_readme = """# Source Code

This directory contains the project's source code.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (project_path / 'src' / 'README.md').write_text(src_readme)
        info("Created src/README.md")
        
        docs_readme = """# Documentation

This directory contains project-specific documentation.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (project_path / 'docs' / 'README.md').write_text(docs_readme)
        info("Created docs/README.md")
        
        tests_readme = """# Tests

This directory contains test files for the project.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (project_path / 'tests' / 'README.md').write_text(tests_readme)
        info("Created tests/README.md")
        
        tools_readme = """# Project-Specific Tools

This directory contains tools and scripts specific to this project. Universal Resonance7 tools are available via the `library/` symlink.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (project_path / 'tools' / 'README.md').write_text(tools_readme)
        info("Created tools/README.md")
        
        # Note: .cursor settings are inherited from workspace root
        info("Using shared .cursor settings from workspace root")
        
        return True
        
    except Exception as e:
        error(f"Failed to create project files: {e}")
        return False

def create_project_template(workspace_root: Path) -> bool:
    """
    Create the project template directory (failsafe only).
    
    Note: The template is tracked in git and should always be present.
    This function only generates it if missing as a failsafe.
    """
    try:
        template_dir = workspace_root / 'library' / 'templates' / 'project_template'
        
        # Check if template already exists (it should be tracked in git)
        if template_dir.exists() and any(template_dir.iterdir()):
            info("Project template already exists (tracked in git)")
            return True
        
        # Only create if missing (failsafe)
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Create template structure
        for dir_name in ['src', 'docs', 'tests', 'tools']:
            (template_dir / dir_name).mkdir(exist_ok=True)
        
        # Create directory READMEs (minimal placeholders)
        src_readme = """# Source Code

This directory contains the project's source code.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (template_dir / 'src' / 'README.md').write_text(src_readme)
        
        tests_readme = """# Tests

This directory contains test files for the project.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (template_dir / 'tests' / 'README.md').write_text(tests_readme)
        
        tools_readme = """# Project-Specific Tools

This directory contains tools and scripts specific to this project. Universal Resonance7 tools are available via the `library/` symlink.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (template_dir / 'tools' / 'README.md').write_text(tools_readme)
        
        docs_readme = """# Documentation

This directory contains project-specific documentation.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (template_dir / 'docs' / 'README.md').write_text(docs_readme)
        
        # Create template README.md (with integrated development log)
        template_readme = """# [Project Name]

[Brief project description - one to three sentences explaining what this project does and its primary purpose.]

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Development Status](#development-status)
- [Development Log](#development-log)
- [Related Sessions](#related-sessions)

---

## Features

- [Feature 1] - [Brief description]
- [Feature 2] - [Brief description]
- [Feature 3] - [Brief description]

---

## Getting Started

### Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]

### Installation

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Quick Start

```bash
# Example command
[command here]
```

---

## Project Structure

```
[project-name]/
├── src/                    # Source code
├── tests/                  # Test files
├── tools/                  # Project-specific tools
├── README.md               # This file
├── requirements.txt        # Python dependencies
│
├── library/                # Symlink → Shared Resonance7 resources
├── sessions/               # Symlink → Shared session management
└── .cursor/                # Symlink → Shared Cursor configuration
```

---

## Usage

[How to use the project - examples, commands, API overview, etc.]

```bash
# Example usage
[example command]
```

---

## Development Status

**Current State**: [Brief status - Working/Broken/In Progress]

**Last Updated**: [YYYY-MM-DD]

**Build Status**: [Success/Failure/Not Tested]

**Known Issues**:
- [Issue 1] - [Brief description]
- [Issue 2] - [Brief description]

---

## Development Log

> **Note**: This log tracks project-wide progress across all sessions. For detailed session-by-session work, see `sessions/current/`.

### Summary

[Main accomplishments, decisions, and key insights across all sessions.]

### Key Decisions & Rationale

- **Decision 1** – [Brief reasoning]
- **Decision 2** – [Brief reasoning]

### Recent Work

#### [YYYY-MM-DD] - [Session ID: YYYYMMDD-NN]
- [What was done in this session]
- [Key changes or additions]
- [Files created/modified]

#### [Previous Session]
- [Previous session work]

### Deliverables & Metrics

- ✅ **Deliverable 1** – [File / feature] — [LoC / size / metric]
- 🚧 **Partial Deliverable** – [Status % or remaining tasks]
- 📊 **Metric** – [Coverage %, build time, etc.]

### Implementation Highlights

- [Notable techniques, libraries, commands, patterns]
- [Key architectural decisions]

### Challenges, Failures & Lessons

#### **Problem [N]: [Brief description]**
- **Issue**: [What went wrong]
- **Root Cause**: [Why it happened]
- **Solution / Work-around**: [How it was fixed]
- **Lesson**: [One-line takeaway]

### Next Work Items

**High Priority**:
- [Task 1]
- [Task 2]

**Medium Priority**:
- [Task 1]
- [Task 2]

**Low Priority**:
- [Task 1]
- [Task 2]

---

## Related Sessions

Session logs documenting work on this project:

- **[YYYYMMDD-NN](sessions/current/YYYYMMDD-NN.md)** – [Brief description of work done]
- **[YYYYMMDD-NN](sessions/current/YYYYMMDD-NN.md)** – [Brief description of work done]
- **[YYYYMMDD-NN](sessions/recent/YYYYMMDD-NN.md)** – [Brief description of work done]

> **Note**: Session logs are automatically archived after 7 days. Older sessions can be found in `sessions/recent/` or `sessions/archived/`.

---

**Part of the Resonance7 framework** - See [root README](../../../README.md) for framework overview.
"""
        (template_dir / 'README.md').write_text(template_readme)
        
        # Create template requirements.txt
        template_requirements = """# [Project Name] Dependencies
# Add your project dependencies here

# Example:
# requests>=2.25.0
# numpy>=1.20.0
"""
        (template_dir / 'requirements.txt').write_text(template_requirements)
        
        # Restore preserved directory READMEs if they were saved
        if hasattr(create_project_template, '_preserved_readmes'):
            for dir_name, readme_content in create_project_template._preserved_readmes.items():
                readme_file = template_dir / dir_name / 'README.md'
                readme_file.parent.mkdir(parents=True, exist_ok=True)
                readme_file.write_text(readme_content, encoding='utf-8')
                info(f"Restored {dir_name}/README.md in template")
            delattr(create_project_template, '_preserved_readmes')
        
        info("Created project template")
        return True
        
    except Exception as e:
        error(f"Failed to create project template: {e}")
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
    print("  - Complete directory structure (src/, docs/, tests/, tools/)")
    print("  - Symlinks to shared Resonance7 resources")
    print("  - README.md with integrated development log")
    print("  - Ready for development")
    print()
    
    return 0

def create_project_template_workflow(dry_run: bool = False) -> int:
    """
    Create the project template (failsafe only).
    
    Note: The template is tracked in git and should always be present.
    This function only generates it if missing as a failsafe.
    """
    workspace_root = find_workspace_root()
    template_dir = workspace_root / 'library' / 'templates' / 'project_template'
    
    show_section_header("Template Creation (Failsafe)")
    print(f"Workspace root: {workspace_root}")
    print(f"Template location: {template_dir}")
    print()
    
    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
        return 0
    
    # Check if template already exists (it should be tracked in git)
    if template_dir.exists() and any(template_dir.iterdir()):
        info("Project template already exists (tracked in git)")
        info("No generation needed - template is present")
        print()
        return 0
    
    # Only generate if missing (failsafe)
    warning("Project template not found - generating as failsafe")
    print("Note: Template should be tracked in git. This is a failsafe regeneration.")
    print()
    
    if not create_project_template(workspace_root):
        return 1
    
    show_section_header("Template Created (Failsafe)")
    print("✅ Generated: library/templates/project_template/")
    print()
    print("The template includes:")
    print("  - Standard project structure")
    print("  - Template configuration files")
    print("  - Ready for copying to new projects")
    print()
    print("⚠️  Note: This template should be tracked in git.")
    print("   If you see this message, the template may be missing from the repository.")
    print()
    
    return 0

def show_main_menu() -> int:
    """Display the main menu and get user choice."""
    print("-" * 64)
    print("  PROJECT SETUP")
    print("-" * 64)
    print()
    print("What would you like to do?")
    print()
    print("1. Create new project workspace")
    print("2. Create project template")
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
    template_dir = workspace_root / 'library' / 'templates' / 'project_template'
    if template_dir.exists():
        print("Template: ✓ library/templates/project_template/")
    else:
        print("Template: ✗ (not created yet)")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Resonance 7 Project Setup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python project_setup.py                    # Interactive mode
  python project_setup.py --project my-app  # Create project directly
  python project_setup.py --template        # Create template only
  python project_setup.py --dry-run         # Preview changes
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
        help='Create project template only'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Preview changes without making them'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='Resonance 7 Project Setup 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Handle direct project creation
    if args.project:
        return setup_new_project(args.project, args.dry_run)
    
    # Handle template creation
    if args.template:
        return create_project_template_workflow(args.dry_run)
    
    # Show header
    workspace_root = find_workspace_root()
    print("=" * 64)
    print("  Resonance 7 - Project Setup Tool")
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
            if create_project_template_workflow(args.dry_run) == 0:
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
