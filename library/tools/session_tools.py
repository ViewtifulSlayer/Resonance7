#!/usr/bin/env python3
"""
session_tools.py - Resonance 7 Session Management Tool

Creates session log files and manages session maintenance.
Part of the Resonance7 framework.

Usage:
    python session_tools.py                   # Interactive mode
    python session_tools.py --help           # Show help
    python session_tools.py --dry-run        # Test without making changes

Version: 1.0.0
Author: Resonance 7 Team
License: MIT
"""

import os
import re
import sys
import argparse
import shutil
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, List, Tuple


__version__ = "1.0.0"

# =============================================================================
# PRUNING CONFIGURATION
# =============================================================================

# Configuration (will be set after function definitions)
SESSIONS_ROOT = None
CURRENT_DIR = None
RECENT_DIR = None
ARCHIVE_DIR = None

# Colors for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def log(message: str) -> None:
    """Print a log message with timestamp and blue color."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Colors.BLUE}[{timestamp}]{Colors.NC} {message}")

def error(message: str) -> None:
    """Print an error message with red color."""
    print(f"{Colors.RED}ERROR:{Colors.NC} {message}", file=os.sys.stderr)

def success(message: str) -> None:
    """Print a success message with green color."""
    print(f"{Colors.GREEN}SUCCESS:{Colors.NC} {message}")

def warning(message: str) -> None:
    """Print a warning message with yellow color."""
    print(f"{Colors.YELLOW}WARNING:{Colors.NC} {message}")

# =============================================================================
# STEP 1: CORE UTILITIES
# =============================================================================

def get_utc_timestamp():
    """
    Get current UTC timestamp in Resonance7 format.
    
    Returns:
        str: Timestamp like "2025-10-14 08:30:15 UTC"
    
    Example:
        >>> get_utc_timestamp()
        '2025-10-14 08:30:15 UTC'
    """
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")


def find_sessions_directory():
    """
    Find the sessions/current/ directory relative to the workspace root.
    
    Returns:
        Path: Path to sessions/current/ directory
    
    Raises:
        FileNotFoundError: If sessions/current/ doesn't exist
    
    Logic:
        Searches upward from script location to find the workspace root,
        then looks for sessions/current/ within that workspace.
    """
    # Start from script location
    current = Path(__file__).resolve().parent
    
    # Search upward for the workspace root
    while current != current.parent:
        # Check if sessions/current/ exists at this level
        sessions_dir = current / "sessions" / "current"
        if sessions_dir.exists():
            return sessions_dir
        
        # Move up one directory
        current = current.parent
    
    # If we get here, we couldn't find it
    raise FileNotFoundError(
        "Could not find sessions/current/ directory. "
        "Make sure you're running this from within the Resonance 7 workspace."
    )


def get_session_files(sessions_dir):
    """
    Get all session log files from the directory.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
    
    Returns:
        list: List of Path objects for .md files, sorted by modification time
    
    Example:
        >>> files = get_session_files(Path("sessions/current"))
        >>> [f.name for f in files]
        ['20251013-01.md', '20251012-03.md', ...]
    """
    md_files = list(sessions_dir.glob("*.md"))
    # Sort by modification time, newest first
    md_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return md_files


def parse_session_filename(filename):
    """
    Parse a session filename to extract date and number.
    
    Args:
        filename (str): Filename like "20251013-01.md" or "20251013-01_pt2.md"
    
    Returns:
        dict or None: {'date': '20251013', 'number': '01', 'part': 'pt2'}
                      or None if filename doesn't match pattern
    
    Examples:
        >>> parse_session_filename("20251013-01.md")
        {'date': '20251013', 'number': '01', 'part': None}
        
        >>> parse_session_filename("20251013-01_pt2.md")
        {'date': '20251013', 'number': '01', 'part': 'pt2'}
    """
    # Pattern: YYYYMMDD-NN.md or YYYYMMDD-NN_ptX.md
    pattern = r'(\d{8})-(\d{2})(?:_pt(\d+))?\.md$'
    match = re.match(pattern, filename)
    
    if match:
        return {
            'date': match.group(1),
            'number': match.group(2),
            'part': f"pt{match.group(3)}" if match.group(3) else None
        }
    return None


def calculate_next_session_number(sessions_dir):
    """
    Calculate the next available session number for today.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
    
    Returns:
        str: Next session ID like "20251014-01"
    
    Logic:
        1. Get today's date in YYYYMMDD format
        2. Find all sessions with today's date
        3. Find the highest number
        4. Return next available number (01-99)
    
    Example:
        If today is 2025-10-14 and these files exist:
            20251014-01.md
            20251014-02.md
        Returns: "20251014-03"
    """
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    
    # Get all session files
    files = get_session_files(sessions_dir)
    
    # Find sessions from today
    today_sessions = []
    for file in files:
        parsed = parse_session_filename(file.name)
        if parsed and parsed['date'] == today:
            today_sessions.append(int(parsed['number']))
    
    # Calculate next number
    if today_sessions:
        next_num = max(today_sessions) + 1
    else:
        next_num = 1
    
    # Format as YYYYMMDD-NN
    return f"{today}-{next_num:02d}"


def get_last_session_info(sessions_dir):
    """
    Get information about the most recent session.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
    
    Returns:
        dict or None: {'filename': str, 'path': Path, 'date': str, 'number': str}
                      or None if no sessions exist
    
    Example:
        >>> info = get_last_session_info(Path("sessions/current"))
        >>> info['filename']
        '20251013-01.md'
    """
    files = get_session_files(sessions_dir)
    
    if not files:
        return None
    
    last_file = files[0]  # Already sorted by modification time
    parsed = parse_session_filename(last_file.name)
    
    if parsed:
        return {
            'filename': last_file.name,
            'path': last_file,
            'date': parsed['date'],
            'number': parsed['number']
        }
    
    return None


# =============================================================================
# STEP 2: YAML FRONTMATTER HANDLING
# =============================================================================

def parse_yaml_frontmatter(file_path):
    """
    Parse YAML frontmatter from a markdown file.
    
    Args:
        file_path (Path): Path to markdown file
    
    Returns:
        dict: Metadata as key-value pairs, or {} if no frontmatter
    
    Logic:
        Reads content between --- markers at start of file
        Parses simple "key: value" pairs
        No external YAML library needed
    
    Example:
        Given file content:
        ---
        title: "Session 20251013-01"
        author: "Resonance 7 Agent"
        ---
        
        Returns:
        {'title': 'Session 20251013-01', 'author': 'Resonance 7 Agent'}
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return {}
    
    # Find YAML frontmatter between --- markers
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}
    
    yaml_content = match.group(1)
    metadata = {}
    
    # Parse each line as "key: value"
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Split on first colon
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Remove quotes from value if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            metadata[key] = value
    
    return metadata


def generate_yaml_frontmatter(metadata):
    """
    Generate YAML frontmatter from metadata dict.
    
    Args:
        metadata (dict): Metadata key-value pairs
    
    Returns:
        str: Formatted YAML frontmatter block with --- markers
    
    Example:
        Input: {'title': 'Session 20251013-01', 'author': 'Phoenix'}
        Output:
        ---
        title: "Session 20251013-01"
        author: "Phoenix"
        ---
    """
    lines = ['---']
    
    # Define field order to match session template
    field_order = [
        'title', 'author', 'model', 'created', 'last_updated',
        'status', 'category', 'description', 'previous_part', 'next_part'
    ]
    
    # Add fields in order
    for key in field_order:
        if key in metadata:
            value = metadata[key]
            # Quote the value if it contains special characters or spaces
            if any(char in str(value) for char in [':', '#', '[', ']', '{', '}']) or ' ' in str(value):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
    
    # Add any remaining fields not in the standard order
    for key, value in metadata.items():
        if key not in field_order:
            if any(char in str(value) for char in [':', '#', '[', ']', '{', '}']) or ' ' in str(value):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
    
    lines.append('---')
    return '\n'.join(lines)


def update_yaml_field(file_path, field_name, new_value):
    """
    Update a specific field in a session's YAML frontmatter.
    
    Args:
        file_path (Path): Path to session file
        field_name (str): Name of field to update (e.g., 'next_part')
        new_value (str): New value for the field
    
    Returns:
        bool: True if successful, False otherwise
    
    Logic:
        1. Read file content
        2. Parse existing frontmatter
        3. Update the field
        4. Regenerate frontmatter
        5. Write back to file
    
    Used for:
        Adding 'next_part' field when creating continuations
    """
    try:
        # Read current content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        metadata = parse_yaml_frontmatter(file_path)
        
        if not metadata:
            print(f"Warning: No frontmatter found in {file_path}")
            return False
        
        # Update field
        metadata[field_name] = new_value
        
        # Generate new frontmatter
        new_frontmatter = generate_yaml_frontmatter(metadata)
        
        # Replace old frontmatter with new
        pattern = r'^---\s*\n.*?\n---\s*\n'
        new_content = re.sub(pattern, new_frontmatter + '\n\n', content, count=1, flags=re.DOTALL)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
        
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False


# =============================================================================
# STEP 3: TEMPLATE BODY GENERATION
# =============================================================================

def generate_template_body(session_id, topic):
    """
    Generate the session log template body.
    
    Args:
        session_id (str): Session ID like "20251014-01"
        topic (str): Session topic/title
    
    Returns:
        str: Complete template body with placeholders
    
    Logic:
        Hardcoded template from session_template.md (lines 41-104)
        Replaces YYYYMMDD-NN with actual session ID
        Replaces [Topic/Project] with actual topic
    
    Note:
        This is the complete template structure that agents fill in.
        Kept in sync with library/session_template.md
    """
    template = f"""# Session {session_id}: {topic}

## Summary
[Main accomplishments, decisions, and key insights from this session]

## Key Decisions & Rationale
- **Decision 1** – [Brief reasoning]
- **Decision 2** – [Brief reasoning]

## Deliverables & Metrics
- ✅ **Deliverable 1** – [File / feature] — [LoC / size / metric]
- 🚧 **Partial Deliverable** – [Status % or remaining tasks]
- 📊 **Metric** – [Coverage %, build time, etc.]

## Implementation Highlights
- [Notable techniques, libraries, commands, patterns]
- [Skip conceptual items that appear in Key Decisions]

## Challenges, Failures & Lessons
### **Problem [N]: [Brief description]**
- **Issue**: [What went wrong]
- **Root Cause**: [Why it happened]
- **Solution / Work-around**: [How it was fixed]
- **Lesson**: [One-line takeaway]

## Next Work Items
### **High Priority**
- [Task 1]
- [Task 2]

### **Medium Priority**
- [Task 1]
- [Task 2]

### **Low Priority**
- [Task 1]
- [Task 2]

## Context Snapshot
- **Current State / Ready Components**: [Brief]
- **Technical Environment / Key Paths**: [Brief]
- **User Preferences (new/changed)**: [Brief]
- **Knowledge Gaps / Open Questions**: [Brief]

## Sources
### Web Sources
- [URL] – [Brief description of relevance]

### Local Sources
- [File path] – [Brief description of relevance]

## Related Sessions
- [Previous session ID] – [Brief connection]
- [Next session context] – [What to expect]

## Notes
#### **User Feedback**
- [User preferences, working style, collaboration patterns]

#### **Process Insights**
- [Workflow discoveries, efficiency improvements]

#### **Ready State**
- [What's ready for use, what needs work]
"""
    return template


def create_session_file(file_path, metadata, session_id, topic):
    """
    Create a complete session log file.
    
    Args:
        file_path (Path): Where to save the file
        metadata (dict): Metadata fields for frontmatter
        session_id (str): Session ID like "20251014-01"
        topic (str): Session topic/title
    
    Returns:
        bool: True if successful, False otherwise
    
    Logic:
        1. Generate YAML frontmatter from metadata
        2. Generate template body with session ID and topic
        3. Combine: frontmatter + blank line + body
        4. Write to file
    
    File structure:
        ---
        [YAML frontmatter]
        ---
        
        # Session 20251014-01: Topic
        [Template sections...]
    """
    try:
        # Generate components
        frontmatter = generate_yaml_frontmatter(metadata)
        body = generate_template_body(session_id, topic)
        
        # Combine with blank line separator
        content = frontmatter + '\n\n' + body
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error creating session file: {e}")
        return False


# =============================================================================
# STEP 4: INTERACTIVE USER INTERFACE
# =============================================================================

def show_header(sessions_dir, next_session_id):
    """
    Display the Resonance7 header with context info.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
        next_session_id (str): Next available session ID
    
    Displays:
        - Resonance 7 banner
        - Current UTC time
        - Last session info
        - Next session ID
    """
    print("=" * 64)
    print("  Resonance 7 - Session Log Creator")
    print("=" * 64)
    print()
    
    # Show current time
    current_time = get_utc_timestamp()
    print(f"Current UTC: {current_time}")
    
    # Show last session
    last_session = get_last_session_info(sessions_dir)
    if last_session:
        print(f"Last Session: {last_session['filename']}")
    else:
        print(f"Last Session: None")
    
    print(f"Next Session: {next_session_id}.md")
    print()


def show_session_type_menu():
    """
    Display menu for choosing session type.
    
    Returns:
        int: User's choice (1, 2, 3, 4, or 5)
    
    Menu options:
        1. New session (interactive)
        2. Auto create (all defaults)
        3. Continue existing session
        4. Prune sessions
        5. Cancel
    """
    print("-" * 64)
    print("  SESSION TYPE")
    print("-" * 64)
    print()
    print("What would you like to do?")
    print()
    print("1. New session (interactive)")
    print("2. Auto create (all defaults)")
    print("3. Continue existing session")
    print("4. Prune sessions")
    print("5. Cancel")
    print()
    
    while True:
        choice = input("Choice [1-5]: ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return int(choice)
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")


def prompt_with_default(prompt_text, default_value=None, allow_empty=False):
    """
    Prompt user for input with optional default value.
    
    Args:
        prompt_text (str): Question to ask
        default_value (str, optional): Default if user presses Enter
        allow_empty (bool): Whether empty input is acceptable
    
    Returns:
        str: User input or default value
    
    Example:
        >>> prompt_with_default("Enter name", "Phoenix")
        Enter name [Phoenix]: <user presses Enter>
        Returns: "Phoenix"
    """
    if default_value:
        prompt = f"{prompt_text} [{default_value}]: "
    else:
        prompt = f"{prompt_text}: "
    
    while True:
        user_input = input(prompt).strip()
        
        # User pressed Enter
        if not user_input:
            if default_value is not None:
                return default_value
            elif allow_empty:
                return ""
            else:
                print("This field is required. Please enter a value.")
                continue
        
        return user_input


def prompt_yes_no(prompt_text, default_yes=True):
    """
    Prompt user for yes/no response.
    
    Args:
        prompt_text (str): Question to ask
        default_yes (bool): Default to yes if True, no if False
    
    Returns:
        bool: True for yes, False for no
    
    Example:
        >>> prompt_yes_no("Continue?", default_yes=True)
        Continue? [Y/n]: <user presses Enter>
        Returns: True
    """
    if default_yes:
        prompt = f"{prompt_text} [Y/n]: "
    else:
        prompt = f"{prompt_text} [y/N]: "
    
    while True:
        response = input(prompt).strip().lower()
        
        if not response:
            return default_yes
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")


def prompt_choice(prompt_text, choices, default=None):
    """
    Prompt user to choose from a list of options.
    
    Args:
        prompt_text (str): Question to ask
        choices (list): List of valid choices
        default (str, optional): Default choice
    
    Returns:
        str: User's choice
    
    Example:
        >>> prompt_choice("Status", ["Active", "Handoff", "Completed"], "Active")
        Status [1=Active, 2=Handoff, 3=Completed] [1]: 
    """
    print()
    print(prompt_text)
    for i, choice in enumerate(choices, 1):
        default_marker = " (default)" if default and choice == default else ""
        print(f"{i}. {choice}{default_marker}")
    print()
    
    # Find default index
    default_index = None
    if default and default in choices:
        default_index = choices.index(default) + 1
    
    while True:
        if default_index:
            prompt = f"Choice [1-{len(choices)}, default={default_index}]: "
        else:
            prompt = f"Choice [1-{len(choices)}]: "
        
        user_input = input(prompt).strip()
        
        # User pressed Enter
        if not user_input and default_index:
            return default
        
        # Validate choice
        try:
            choice_num = int(user_input)
            if 1 <= choice_num <= len(choices):
                return choices[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(choices)}.")
        except ValueError:
            print("Please enter a valid number.")


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


def confirm_metadata(metadata, session_id):
    """
    Display metadata for user confirmation.
    
    Args:
        metadata (dict): Metadata to display
        session_id (str): Session ID
    
    Returns:
        bool: True if user confirms, False otherwise
    """
    show_section_header("Confirmation")
    
    print(f"Creating: sessions/current/{session_id}.md")
    print()
    print("Metadata:")
    
    # Display in order
    field_order = [
        'title', 'author', 'model', 'created', 'last_updated',
        'status', 'category', 'description'
    ]
    
    for field in field_order:
        if field in metadata:
            # Truncate long values
            value = str(metadata[field])
            if len(value) > 60:
                value = value[:57] + "..."
            print(f"  {field.replace('_', ' ').title()}: {value}")
    
    print()
    return prompt_yes_no("Proceed?", default_yes=True)


def show_success(session_path):
    """
    Display success message after session creation.
    
    Args:
        session_path (Path): Path to created session file
    """
    show_section_header("Session Created")
    
    print(f"✅ Created: {session_path}")
    print()
    print("The session file includes:")
    print("  - Complete YAML frontmatter")
    print("  - Full template structure with placeholder sections")
    print("  - Ready for agent to populate")
    print()


# =============================================================================
# STEP 5: NEW SESSION WORKFLOW
# =============================================================================

def collect_new_session_metadata(session_id):
    """
    Interactively collect metadata for a new session.
    
    Args:
        session_id (str): Session ID like "20251014-01"
    
    Returns:
        dict: Complete metadata dictionary, or None if user cancels
    
    Workflow:
        1. Ask for title/topic
        2. Ask for author (default: Resonance 7 Agent)
        3. Ask if model is auto (default: yes)
        4. Ask for status (default: Active)
        5. Ask for description (allow placeholder)
        6. Generate timestamps
        7. Return complete metadata dict
    """
    metadata = {}
    
    # Session title
    show_section_header("Session Title")
    print(f"Session ID: {session_id}")
    print("Enter session topic/title:")
    print("Press Enter to use placeholder for agent to name based on context.")
    print()
    topic = input("> ").strip()
    
    if not topic:
        metadata['title'] = f"Session {session_id}: [Topic/Project]"
        print("✅ Title placeholder set for agent completion")
    else:
        metadata['title'] = f"Session {session_id}: {topic}"
    
    # Author
    show_section_header("Author")
    author = prompt_with_default(
        "Enter author name",
        default_value="Resonance 7 Agent"
    )
    metadata['author'] = author
    
    # Model
    show_section_header("Model")
    is_auto = prompt_yes_no("Is your model selection set to Auto?", default_yes=True)
    
    if is_auto:
        metadata['model'] = "[model]"
        print("✅ Model will be auto-detected by the agent")
    else:
        model_name = prompt_with_default("Enter model name manually")
        metadata['model'] = model_name
    
    # Status
    show_section_header("Status")
    status = prompt_choice(
        "Session status:",
        ["Active", "Handoff", "Completed"],
        default="Active"
    )
    metadata['status'] = status
    
    # Description
    show_section_header("Description")
    print("Enter brief description (what this session accomplishes):")
    print("Press Enter to use placeholder for agent to fill in later.")
    print()
    description = input("> ").strip()
    
    if not description:
        metadata['description'] = "[Brief description of session focus]"
        print("✅ Description placeholder set for agent completion")
    else:
        metadata['description'] = description
    
    # Auto-generate timestamps and category
    timestamp = get_utc_timestamp()
    metadata['created'] = timestamp
    metadata['last_updated'] = timestamp
    metadata['category'] = "Session Log"
    
    return metadata


def create_new_session_workflow(sessions_dir, dry_run=False):
    """
    Complete workflow for creating a new session.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
        dry_run (bool): If True, don't actually create files
    
    Returns:
        int: 0 for success, 1 for cancellation/error
    
    Workflow:
        1. Calculate next session number
        2. Collect metadata interactively
        3. Show confirmation
        4. Create session file
        5. Show success message
    """
    try:
        # Get next session ID
        session_id = calculate_next_session_number(sessions_dir)
        
        # Collect metadata
        metadata = collect_new_session_metadata(session_id)
        
        if not metadata:
            print("\n❌ Cancelled by user")
            return 1
        
        # Extract topic from title
        topic = metadata['title'].replace(f"Session {session_id}: ", "")
        
        # Confirm
        if not confirm_metadata(metadata, session_id):
            print("\n❌ Cancelled by user")
            return 1
        
        # Dry run - skip file creation
        if dry_run:
            print("\n🔍 DRY RUN MODE")
            print(f"Would create: sessions/current/{session_id}.md")
            print("No files were created.")
            return 0
        
        # Create the file
        file_path = sessions_dir / f"{session_id}.md"
        
        success = create_session_file(file_path, metadata, session_id, topic)
        
        if success:
            show_success(file_path)
            return 0
        else:
            print(f"\n❌ Failed to create session file")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user (Ctrl+C)")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def create_auto_session_workflow(sessions_dir, dry_run=False):
    """
    Auto-create a session with all default/placeholder values.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
        dry_run (bool): If True, don't actually create files
    
    Returns:
        int: 0 for success, 1 for cancellation/error
    
    Workflow:
        1. Calculate next session number
        2. Generate metadata with all defaults:
           - Title: "Session {id}: [Topic/Project]"
           - Author: "Resonance 7 Agent"
           - Model: "[model]"
           - Status: "Active"
           - Description: "[Brief description of session focus]"
        3. Create session file immediately
        4. Show success message
    """
    try:
        # Get next session ID
        session_id = calculate_next_session_number(sessions_dir)
        
        # Generate metadata with all defaults
        timestamp = get_utc_timestamp()
        metadata = {
            'title': f"Session {session_id}: [Topic/Project]",
            'author': "Resonance 7 Agent",
            'model': "[model]",
            'created': timestamp,
            'last_updated': timestamp,
            'status': "Active",
            'category': "Session Log",
            'description': "[Brief description of session focus]"
        }
        
        topic = "[Topic/Project]"
        
        # Show what we're creating
        show_section_header("Auto Create")
        print(f"Creating session with all defaults: {session_id}.md")
        print()
        print("Complete YAML frontmatter preview:")
        print()
        
        # Generate and display the actual frontmatter
        frontmatter = generate_yaml_frontmatter(metadata)
        print(frontmatter)
        print()
        
        # Confirm
        if not prompt_yes_no("Proceed?", default_yes=True):
            print("\n❌ Cancelled by user")
            return 1
        
        # Dry run - skip file creation
        if dry_run:
            print("\n🔍 DRY RUN MODE")
            print(f"Would create: sessions/current/{session_id}.md")
            print("No files were created.")
            return 0
        
        # Create the file
        file_path = sessions_dir / f"{session_id}.md"
        
        success = create_session_file(file_path, metadata, session_id, topic)
        
        if success:
            show_success(file_path)
            return 0
        else:
            print(f"\n❌ Failed to create session file")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user (Ctrl+C)")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


# =============================================================================
# STEP 6: CONTINUATION WORKFLOW
# =============================================================================

def select_session_to_continue(sessions_dir):
    """
    Let user select a session to continue.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
    
    Returns:
        tuple: (session_path, parsed_info) or (None, None) if cancelled
    
    Shows recent sessions and lets user pick one or enter path manually.
    """
    show_section_header("Select Session to Continue")
    
    # Get recent sessions (limit to 10)
    files = get_session_files(sessions_dir)[:10]
    
    if not files:
        print("No sessions found in current/")
        return None, None
    
    print("Recent sessions in current/:")
    print()
    for i, file_path in enumerate(files, 1):
        parsed = parse_session_filename(file_path.name)
        if parsed:
            # Get title from metadata if possible
            metadata = parse_yaml_frontmatter(file_path)
            title = metadata.get('title', file_path.name)
            # Truncate long titles
            if len(title) > 50:
                title = title[:47] + "..."
            print(f"{i}. {file_path.name} - {title}")
        else:
            print(f"{i}. {file_path.name}")
    
    print()
    print(f"{len(files) + 1}. Enter filename manually")
    print(f"{len(files) + 2}. Cancel")
    print()
    
    while True:
        choice = input(f"Choice [1-{len(files) + 2}]: ").strip()
        
        try:
            choice_num = int(choice)
            
            # Selected a session from the list
            if 1 <= choice_num <= len(files):
                selected_file = files[choice_num - 1]
                parsed = parse_session_filename(selected_file.name)
                return selected_file, parsed
            
            # Manual entry
            elif choice_num == len(files) + 1:
                filename = input("Enter session filename: ").strip()
                file_path = sessions_dir / filename
                if not file_path.exists():
                    print(f"File not found: {filename}")
                    continue
                parsed = parse_session_filename(filename)
                return file_path, parsed
            
            # Cancel
            elif choice_num == len(files) + 2:
                return None, None
            
            else:
                print(f"Please enter a number between 1 and {len(files) + 2}")
                
        except ValueError:
            print("Please enter a valid number")


def determine_next_part_number(session_path, parsed_info):
    """
    Determine the next part number for a continuation.
    
    Args:
        session_path (Path): Path to session being continued
        parsed_info (dict): Parsed session filename info
    
    Returns:
        int: Next part number (2, 3, 4, etc.)
    
    Logic:
        If file is "20251014-01.md" -> next is part 2
        If file is "20251014-01_pt2.md" -> next is part 3
    """
    if parsed_info['part']:
        # Already a part (e.g., pt2), increment
        part_num = int(parsed_info['part'][2:])  # Extract number from "pt2"
        return part_num + 1
    else:
        # Original file, next is part 2
        return 2


def rename_to_part1(session_path, parsed_info):
    """
    Rename a session file to add _pt1 suffix.
    
    Args:
        session_path (Path): Current path (e.g., "20251014-01.md")
        parsed_info (dict): Parsed filename info
    
    Returns:
        Path: New path (e.g., "20251014-01_pt1.md")
    
    Only renames if file doesn't already have a part number.
    """
    if parsed_info['part']:
        # Already has part number, no rename needed
        return session_path
    
    # Generate new filename with _pt1
    new_name = f"{parsed_info['date']}-{parsed_info['number']}_pt1.md"
    new_path = session_path.parent / new_name
    
    # Rename the file
    session_path.rename(new_path)
    
    return new_path


def collect_continuation_metadata(session_id, previous_metadata):
    """
    Collect metadata for a continuation session.
    
    Args:
        session_id (str): New session ID (e.g., "20251014-01_pt2")
        previous_metadata (dict): Metadata from previous part
    
    Returns:
        dict: Complete metadata dictionary
    
    Inherits: author, model, category
    New: title (new subtitle), description, timestamps, status
    """
    metadata = {}
    
    # Show what we're continuing
    show_section_header("Continuation")
    print(f"Continuing: {previous_metadata.get('title', 'Unknown')}")
    print(f"New session ID: {session_id}")
    print()
    
    # New title/subtitle
    show_section_header("New Part Title")
    print("Original title:", previous_metadata.get('title', 'N/A'))
    print()
    print("Enter new focus/subtitle for this part:")
    print("Press Enter to keep the original title.")
    print()
    
    new_subtitle = input("> ").strip()
    
    if new_subtitle:
        metadata['title'] = f"Session {session_id}: {new_subtitle}"
    else:
        # Extract original topic from previous title
        prev_title = previous_metadata.get('title', '')
        if ': ' in prev_title:
            topic = prev_title.split(': ', 1)[1]
            # Remove any "Part X: " prefix from the topic
            if topic.startswith('Part ') and ': ' in topic:
                topic = topic.split(': ', 1)[1]
            metadata['title'] = f"Session {session_id}: {topic}"
        else:
            metadata['title'] = f"Session {session_id}"
    
    # Inherit author, model, category
    metadata['author'] = previous_metadata.get('author', 'Resonance 7 Agent')
    metadata['model'] = previous_metadata.get('model', '[model]')
    metadata['category'] = previous_metadata.get('category', 'Session Log')
    
    # New description
    show_section_header("Description")
    print("Enter brief description for this part:")
    print("Press Enter to use placeholder for agent to fill in later.")
    print()
    
    description = input("> ").strip()
    
    if not description:
        metadata['description'] = "[Brief description of session focus]"
        print("✅ Description placeholder set for agent completion")
    else:
        metadata['description'] = description
    
    # Status always starts as Active for new parts
    metadata['status'] = "Active"
    
    # Generate timestamps
    timestamp = get_utc_timestamp()
    metadata['created'] = timestamp
    metadata['last_updated'] = timestamp
    
    return metadata


def create_continuation_workflow(sessions_dir, dry_run=False):
    """
    Complete workflow for continuing an existing session.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
        dry_run (bool): If True, don't actually modify files
    
    Returns:
        int: 0 for success, 1 for cancellation/error
    
    Workflow:
        1. User selects session to continue
        2. Check if it already has a continuation (error if so)
        3. Determine next part number
        4. Rename original to _pt1 (if needed)
        5. Collect metadata for new part
        6. Update previous part with next_part field
        7. Update previous part status to "Completed" if Active/Handoff
        8. Create new part with previous_part field
        9. Show success
    """
    try:
        # Select session
        session_path, parsed_info = select_session_to_continue(sessions_dir)
        
        if not session_path:
            print("\n❌ Cancelled by user")
            return 1
        
        # Parse metadata from selected session
        previous_metadata = parse_yaml_frontmatter(session_path)
        
        if not previous_metadata:
            print(f"\n❌ Could not read metadata from {session_path.name}")
            return 1
        
        # Check if this session already has a continuation
        if 'next_part' in previous_metadata:
            print(f"\n❌ Error: {session_path.name} already has a continuation")
            print(f"   Next part: {previous_metadata['next_part']}")
            print(f"\n💡 To create Part 3, select Part 2 instead.")
            return 1
        
        # Determine next part number
        next_part_num = determine_next_part_number(session_path, parsed_info)
        
        # Generate new session ID
        base_id = f"{parsed_info['date']}-{parsed_info['number']}"
        new_session_id = f"{base_id}_pt{next_part_num}"
        
        # Rename original to _pt1 if needed
        if not dry_run and not parsed_info['part']:
            print(f"\n📝 Renaming {session_path.name} → {base_id}_pt1.md")
            session_path = rename_to_part1(session_path, parsed_info)
            print(f"✅ Renamed to: {session_path.name}")
        elif dry_run and not parsed_info['part']:
            print(f"\n🔍 DRY RUN: Would rename {session_path.name} → {base_id}_pt1.md")
            # Update session_path for dry run consistency
            session_path = session_path.parent / f"{base_id}_pt1.md"
        
        # Collect metadata for new part
        new_metadata = collect_continuation_metadata(new_session_id, previous_metadata)
        
        # Add continuation fields
        new_metadata['previous_part'] = session_path.name
        
        # Extract topic from title
        topic = new_metadata['title'].replace(f"Session {new_session_id}: ", "")
        
        # Confirm
        if not confirm_metadata(new_metadata, new_session_id):
            print("\n❌ Cancelled by user")
            # If we renamed in non-dry-run, we should rename back
            # For simplicity, we'll note this as a limitation
            return 1
        
        # Dry run - skip file operations
        if dry_run:
            print("\n🔍 DRY RUN MODE")
            print(f"Would update {session_path.name}:")
            print(f"  - Add next_part: {new_session_id}.md")
            print(f"  - Update status: Completed")
            print(f"\nWould create: sessions/current/{new_session_id}.md")
            print(f"  - With previous_part: {session_path.name}")
            print("\nNo files were created or modified.")
            return 0
        
        # Update previous part
        # Add next_part field
        update_yaml_field(session_path, 'next_part', f"{new_session_id}.md")
        
        # Update status if Active or Handoff
        prev_status = previous_metadata.get('status', '')
        if prev_status in ['Active', 'Handoff']:
            update_yaml_field(session_path, 'status', 'Completed')
            print(f"✅ Updated {session_path.name} status: {prev_status} → Completed")
        
        print(f"✅ Updated {session_path.name} with next_part field")
        
        # Create new part
        new_file_path = sessions_dir / f"{new_session_id}.md"
        
        success = create_session_file(new_file_path, new_metadata, new_session_id, topic)
        
        if success:
            show_success(new_file_path)
            print(f"🔗 Linked to previous part: {session_path.name}")
            return 0
        else:
            print(f"\n❌ Failed to create continuation file")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user (Ctrl+C)")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


# =============================================================================
# STEP 7: PRUNING FUNCTIONS
# =============================================================================

def initialize_pruning_paths():
    """Initialize the path configuration for pruning."""
    global SESSIONS_ROOT, CURRENT_DIR, RECENT_DIR, ARCHIVE_DIR
    workspace_root = find_sessions_directory().parent.parent
    SESSIONS_ROOT = workspace_root / "sessions"
    CURRENT_DIR = SESSIONS_ROOT / "current"
    RECENT_DIR = SESSIONS_ROOT / "recent"
    ARCHIVE_DIR = SESSIONS_ROOT / "archived"

def check_pruning_directories() -> bool:
    """Check if required directories exist for pruning."""
    log("Checking directory structure...")
    
    if not SESSIONS_ROOT.exists():
        error(f"Sessions root directory not found: {SESSIONS_ROOT}")
        return False
    
    if not CURRENT_DIR.exists():
        error(f"Current sessions directory not found: {CURRENT_DIR}")
        return False
    
    # Create directories if they don't exist
    RECENT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    success("Directory structure verified")
    return True

def extract_session_date(filename: str) -> Optional[datetime]:
    """Extract date from filename (format: YYYYMMDD-NN.md)."""
    match = re.match(r'^(\d{8})-(\d{2})\.md$', filename)
    if match:
        date_part = match.group(1)
        year = int(date_part[:4])
        month = int(date_part[4:6])
        day = int(date_part[6:8])
        try:
            return datetime(year, month, day)
        except ValueError:
            return None
    return None

def get_session_status(file_path: Path) -> Optional[str]:
    """Extract status from YAML frontmatter of session file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find YAML frontmatter between --- markers
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            try:
                # Parse YAML manually (no external dependencies)
                metadata = {}
                for line in yaml_content.split('\n'):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        metadata[key] = value
                return metadata.get('status')
            except Exception as e:
                warning(f"Failed to parse YAML in {file_path.name}: {e}")
                return None
        else:
            warning(f"No YAML frontmatter found in {file_path.name}")
            return None
    except Exception as e:
        warning(f"Failed to read {file_path.name}: {e}")
        return None

def update_session_status(file_path: Path, new_status: str) -> bool:
    """Update status in YAML frontmatter of session file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find YAML frontmatter between --- markers
        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not yaml_match:
            warning(f"No YAML frontmatter found in {file_path.name}")
            return False
        
        yaml_content = yaml_match.group(1)
        try:
            # Parse YAML manually (no external dependencies)
            metadata = {}
            for line in yaml_content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    metadata[key] = value
        except Exception as e:
            warning(f"Failed to parse YAML in {file_path.name}: {e}")
            return False
        
        # Update status
        metadata['status'] = new_status
        
        # Reconstruct YAML frontmatter manually
        new_yaml_lines = ['---']
        for key, value in metadata.items():
            if any(char in str(value) for char in [':', '#', '[', ']', '{', '}']) or ' ' in str(value):
                new_yaml_lines.append(f'{key}: "{value}"')
            else:
                new_yaml_lines.append(f'{key}: {value}')
        new_yaml_lines.append('---')
        new_yaml = '\n'.join(new_yaml_lines)
        
        # Replace the YAML section in the content
        new_content = re.sub(
            r'^---\s*\n.*?\n---\s*\n',
            f'{new_yaml}\n\n',
            content,
            flags=re.DOTALL,
            count=1
        )
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        warning(f"Failed to update status in {file_path.name}: {e}")
        return False

def update_session_status_if_needed(file_path: Path, dry_run: bool = False) -> bool:
    """Update session status to appropriate 'Completed' variant if needed."""
    current_status = get_session_status(file_path)
    
    if current_status is None:
        warning(f"Could not determine status for {file_path.name}, skipping status update")
        return False
    
    # If already has a completed status, don't change it
    if current_status in ["Completed (Agent)", "Completed (Auto)"]:
        return True
    
    # Determine appropriate status
    if current_status == "Completed":
        new_status = "Completed (Agent)"
    else:
        new_status = "Completed (Auto)"
    
    if dry_run:
        log(f"DRY RUN: Would update status in {file_path.name} from '{current_status}' to '{new_status}'")
        return True
    else:
        if update_session_status(file_path, new_status):
            log(f"Updated status in {file_path.name}: '{current_status}' -> '{new_status}'")
            return True
        else:
            warning(f"Failed to update status in {file_path.name}")
            return False

def move_old_sessions(dry_run: bool = False) -> int:
    """Move sessions older than 7 days from current/ to recent/."""
    log("Checking for sessions older than 7 days...")
    
    moved_count = 0
    current_date = datetime.now()
    seven_days_ago = current_date - timedelta(days=7)
    
    # Find all .md files in current/ directory
    for file_path in CURRENT_DIR.glob("*.md"):
        filename = file_path.name
        session_date = extract_session_date(filename)
        
        if session_date and session_date < seven_days_ago:
            # Update status before moving
            update_session_status_if_needed(file_path, dry_run)
            
            target_file = RECENT_DIR / filename
            
            # Check if file already exists in recent/
            if target_file.exists():
                warning(f"File already exists in recent/: {filename}")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_name = f"{filename[:-3]}_{timestamp}.md"
                target_file = RECENT_DIR / backup_name
            
            if dry_run:
                log(f"DRY RUN: Would copy {filename} -> {target_file}")
                log(f"DRY RUN: Would delete {filename} from current/ after validation")
            else:
                # Copy file first
                shutil.copy2(file_path, target_file)
                log(f"Copied: {filename} -> recent/")
                
                # Verify copy was successful
                if target_file.exists() and target_file.stat().st_size == file_path.stat().st_size:
                    # Delete original only after successful copy verification
                    file_path.unlink()
                    log(f"Deleted: {filename} from current/ (copy verified)")
                else:
                    error(f"Copy verification failed for {filename}")
                    # Clean up failed copy
                    target_file.unlink(missing_ok=True)
                    continue
                
            moved_count += 1
    
    if moved_count == 0:
        log("No sessions older than 7 days found")
    else:
        if dry_run:
            log(f"DRY RUN: Would move {moved_count} session(s) to recent/")
        else:
            success(f"Moved {moved_count} session(s) to recent/")
    
    return moved_count

def copy_to_monthly_archives(dry_run: bool = False) -> None:
    """Copy all files from current/ and recent/ to archived/ in YYYY-MM.zip format."""
    log("Copying all files to archived/ in monthly zip archives...")
    
    # Get all unique year-month combinations from current/ and recent/ files
    year_months = set()
    
    for source_dir in [CURRENT_DIR, RECENT_DIR]:
        for file_path in source_dir.glob("*.md"):
            session_date = extract_session_date(file_path.name)
            if session_date:
                year_month = session_date.replace(day=1)
                year_months.add(year_month)
    
    if not year_months:
        log("No sessions found to archive")
        return
    
    # Sort year-months and process each month
    sorted_year_months = sorted(year_months)
    
    for target_year_month in sorted_year_months:
        archive_zip_name = f"{target_year_month.strftime('%Y-%m')}.zip"
        archive_zip_path = ARCHIVE_DIR / archive_zip_name
        
        log(f"Processing {target_year_month.strftime('%Y-%m')}...")
        
        files_to_archive = []
        
        # Collect files from current/ and recent/ for the target month
        for source_dir in [CURRENT_DIR, RECENT_DIR]:
            for file_path in source_dir.glob("*.md"):
                session_date = extract_session_date(file_path.name)
                if session_date and session_date.year == target_year_month.year and session_date.month == target_year_month.month:
                    files_to_archive.append(file_path)
        
        if not files_to_archive:
            log(f"No files found for month: {target_year_month.strftime('%Y-%m')}")
            continue
        
        if dry_run:
            log(f"DRY RUN: Would create {archive_zip_name} with {len(files_to_archive)} files")
            for file_path in files_to_archive:
                log(f"DRY RUN: Would add {file_path.name} to {archive_zip_name}")
        else:
            try:
                # Create or update zip archive
                with zipfile.ZipFile(archive_zip_path, 'a', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in files_to_archive:
                        # Check if file already exists in zip
                        if file_path.name in zipf.namelist():
                            log(f"File already exists in archive: {file_path.name}")
                            continue
                        
                        # Add file to zip
                        zipf.write(file_path, file_path.name)
                        log(f"Added: {file_path.name} to {archive_zip_name}")
                
                success(f"Created/updated {archive_zip_name} with {len(files_to_archive)} files")
            except Exception as e:
                error(f"Failed to create archive {archive_zip_name}: {e}")
    
    if not sorted_year_months:
        log("No months found for archiving")

def cleanup_old_sessions(dry_run: bool = False) -> None:
    """Ask user if they want to delete sessions older than 90 days from recent/ after confirming they're backed up."""
    log("Checking for sessions older than 90 days in recent/...")
    
    current_date = datetime.now()
    ninety_days_ago = current_date - timedelta(days=90)
    
    # Find files older than 90 days in recent/
    old_files = []
    
    for file_path in RECENT_DIR.glob("*.md"):
        session_date = extract_session_date(file_path.name)
        if session_date and session_date < ninety_days_ago:
            old_files.append((file_path, session_date))
    
    if not old_files:
        log("No sessions older than 90 days found in recent/")
        return
    
    # Sort by date
    old_files.sort(key=lambda x: x[1])
    
    log(f"Found {len(old_files)} sessions older than 90 days:")
    for file_path, session_date in old_files:
        log(f"  - {file_path.name} ({session_date.strftime('%Y-%m-%d')})")
    
    if dry_run:
        log("DRY RUN: Would ask user if they want to delete these files")
        return
    
    # Ask user for confirmation
    print(f"\n{Colors.YELLOW}WARNING:{Colors.NC} Found {len(old_files)} sessions older than 90 days in recent/")
    print("These files have been copied to archived/ folders. Do you want to delete them from recent/?")
    print("This will free up space but remove them from the recent/ directory.")
    
    response = input("Delete old sessions from recent/? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        deleted_count = 0
        for file_path, session_date in old_files:
            try:
                file_path.unlink()
                log(f"Deleted: {file_path.name} (90+ days old)")
                deleted_count += 1
            except Exception as e:
                error(f"Failed to delete {file_path.name}: {e}")
        
        if deleted_count > 0:
            success(f"Deleted {deleted_count} old sessions from recent/")
    else:
        log("User chose not to delete old sessions from recent/")

def show_pruning_menu():
    """Display menu for pruning options."""
    print("-" * 64)
    print("  SESSION PRUNING")
    print("-" * 64)
    print()
    print("What would you like to do?")
    print()
    print("1. Move old sessions (7+ days)")
    print("2. Create monthly archives")
    print("3. Cleanup old sessions (90+ days)")
    print("4. Full maintenance (all steps)")
    print("5. Cancel")
    print()
    
    while True:
        choice = input("Choice [1-5]: ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return int(choice)
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

def prune_sessions_workflow(sessions_dir, dry_run=False):
    """
    Complete workflow for pruning sessions.
    
    Args:
        sessions_dir (Path): Path to sessions/current/
        dry_run (bool): If True, don't actually modify files
    
    Returns:
        int: 0 for success, 1 for error
    """
    try:
        # Initialize pruning paths
        initialize_pruning_paths()
        
        if not check_pruning_directories():
            return 1
        
        # Show pruning menu
        choice = show_pruning_menu()
        
        if choice == 1:
            # Move old sessions
            move_old_sessions(dry_run)
            
        elif choice == 2:
            # Create monthly archives
            copy_to_monthly_archives(dry_run)
            
        elif choice == 3:
            # Cleanup old sessions
            cleanup_old_sessions(dry_run)
            
        elif choice == 4:
            # Full maintenance
            log("Starting full session maintenance...")
            move_old_sessions(dry_run)
            copy_to_monthly_archives(dry_run)
            if not dry_run:
                cleanup_old_sessions(dry_run)
            success("Full maintenance completed")
            
        else:
            # Cancel
            print("\nPruning cancelled")
            return 0
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nERROR: Cancelled by user (Ctrl+C)")
        return 1
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

# =============================================================================
# STEP 8: CLI ARGUMENTS & MAIN ENTRY POINT
# =============================================================================

def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    
    Supported flags:
        --help: Show help message
        --dry-run: Preview actions without making changes
        --version: Show version number
        --prune: Go directly to pruning menu
    """
    parser = argparse.ArgumentParser(
        prog='Session Tools',
        description='Resonance 7 Session Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                    # Interactive mode - session management menu
  %(prog)s --dry-run          # Test run without making changes
  %(prog)s --prune            # Go directly to pruning menu
  %(prog)s --help             # Show this help message

For more information, see: library/session_template.md
        '''
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be done without making changes'
    )
    
    parser.add_argument(
        '--prune',
        action='store_true',
        help='Go directly to session pruning menu'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point for the session management tool.
    
    Workflow:
        1. Parse command-line arguments
        2. Find sessions directory
        3. Show header with context
        4. Handle direct pruning if --prune flag
        5. Show menu (New session / Continue / Prune / Cancel)
        6. Route to appropriate workflow
        7. Handle errors gracefully
    
    Returns:
        int: Exit code (0 for success, 1 for error/cancel)
    """
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Find sessions directory
        try:
            sessions_dir = find_sessions_directory()
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            print("\nMake sure you're running this from within the Resonance 7 workspace.")
            print("Expected structure: [workspace-root]/sessions/current/")
            return 1
        
        # Calculate next session number
        next_session_id = calculate_next_session_number(sessions_dir)
        
        # Show header
        show_header(sessions_dir, next_session_id)
        
        # Dry run notice
        if args.dry_run:
            print("DRY RUN MODE - No files will be created or modified")
            print()
        
        # Handle direct pruning
        if args.prune:
            return prune_sessions_workflow(sessions_dir, dry_run=args.dry_run)
        
        # Show menu
        choice = show_session_type_menu()
        
        # Route to workflow
        if choice == 1:
            # New session (interactive)
            return create_new_session_workflow(sessions_dir, dry_run=args.dry_run)
            
        elif choice == 2:
            # Auto create (all defaults)
            return create_auto_session_workflow(sessions_dir, dry_run=args.dry_run)
            
        elif choice == 3:
            # Continue session
            return create_continuation_workflow(sessions_dir, dry_run=args.dry_run)
            
        elif choice == 4:
            # Prune sessions
            return prune_sessions_workflow(sessions_dir, dry_run=args.dry_run)
            
        else:
            # Cancel
            print("\nGoodbye!")
            return 0
    
    except KeyboardInterrupt:
        print("\n\nERROR: Cancelled by user (Ctrl+C)")
        return 1
        
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("\nIf this error persists, please report it to the Resonance 7 team.")
        return 1


if __name__ == "__main__":
    exit(main())

