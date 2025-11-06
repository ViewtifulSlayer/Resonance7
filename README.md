Resonance7/                         # Main workspace
├── .cursor/                         # Shared Cursor configuration
│   └── rules/  
│       └── agent_onboarding.mdc     # Shared Cursor rules (IDE-agnostic protocol)
├── library/                         # Shared Resonance 7 resources
│   ├── docs/                        # Knowledge base modules (see docs/README.md)
│   ├── agent_foundation.json         # Core Resonance 7 Agent foundation
│   ├── session_template.md           # Session logging template
│   ├── workspace_template/           # Project template (see workspace_template/README.md)
│   └── README.md                     # Documentation for library directory
├── sessions/                         # Shared session management
│   ├── current/                      # Current sessions (last 7 days)
│   ├── recent/                       # Sessions 7+ days old
│   ├── archived/                     # Monthly zip archives (YYYY-MM.zip)
│   └── README.md                     # Documentation for sessions directory
├── tools/                            # Shared scripts and tools
│   ├── session_tools.py              # Script for session log management
│   ├── setup_workspace.py            # Workspace setup and template management
│   └── README.md                     # Documentation for session tools
├── projects/                         # Project-specific workspaces
│   └── [project-name]/               # Individual user projects
│       ├── src/                      # Project source code
│       ├── docs/                     # Project documentation
│       ├── tests/                    # Project tests
│       ├── .gitignore                # Project-level git ignore
│       └── README.md                 # Project README
│       # Note: library/, sessions/, tools/, .cursor/ are symlinked into projects
├── .cursorignore                     # Root-level Cursor ignore file
├── .agentignore                      # Root-level agent ignore file
├── .gitignore                        # Root-level git ignore file
├── .gitattributes                    # Git attributes for line endings
├── LICENSE                           # MIT License
└── README.md                         # Root-level README file

## Future Considerations

### GitHub Actions Workflows
GitHub Actions workflows (`.github/workflows/`) can be added for automated validation and CI/CD:
- Validate session log YAML frontmatter
- Check session chain integrity
- Generate session statistics and reports
- Automated testing and quality checks
