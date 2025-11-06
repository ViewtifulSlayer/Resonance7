# Library Documentation Modules

This directory is intended for knowledge base and context modules that provide agents with reference documentation, examples, and domain-specific information.

## Purpose

The `docs/` directory serves as a shared knowledge repository accessible to all projects via symlinks. This allows agents to access relevant documentation and examples without duplicating content across projects.

## Architecture

Documentation modules are organized by category:
- **`languages/`** - Programming language documentation and examples
- **`frameworks/`** - Framework and library documentation
- **`hardware/`** - Hardware documentation and service manuals
- **`tools/`** - Development tool documentation
- **`subjects/`** - Domain-specific knowledge modules

## Usage Model

Modules should be downloaded on-demand rather than included in the base Resonance 7 repository:

1. **Identify needed modules** - Determine which documentation modules are relevant to your work
2. **Download modules** - Use the module download tool (planned) to fetch specific modules from the Resonance 7 documentation repository
3. **Automatic access** - Modules become available to all projects via the shared `library/` symlink

## Future Tooling

A module management tool is planned that will:
- Download specific documentation modules from a GitHub repository
- Manage module versions and updates
- Keep the repository lean by only including modules as needed
- Provide a catalog of available modules

## For GitHub Repository

This directory is included in the Resonance 7 repository to establish the structure and purpose. The actual documentation modules are maintained separately and downloaded as needed.

## Integration

Once modules are present, they are automatically accessible to:
- All projects via the shared `library/` symlink
- Agents working in any Resonance 7 workspace
- Tools that reference documentation for context

## Best Practices

- Keep modules focused and modular
- Only download modules you actually need
- Update modules periodically to stay current
- Contribute new modules back to the community repository

