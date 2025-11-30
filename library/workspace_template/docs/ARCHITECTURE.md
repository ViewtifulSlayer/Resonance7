# Architecture Documentation

## Overview

[Project Name] is a [brief description of what the project does]. [Optional: Describe the core approach or methodology used.]

**Data Source**: [Describe primary data source]
- **Location**: `data/raw/[filename]`
- **Size**: [if applicable]
- **Format**: [data format: JSON, XML, CSV, database, API, etc.]
- **Update Frequency**: [how often data is updated]

**Target Platform**: [deployment target: GitHub Pages, web server, desktop app, etc.]
- **Limits/Constraints**: [any platform-specific limits]
- **Current Data Size**: [if applicable]

## System Architecture

### High-Level Flow

```
[Data Source] → [Stage 1] → [Stage 2] → [Stage 3] → [Output/Application]
```

[Describe each stage in the pipeline]

1. **[Stage 1 Name]** (`src/[script_name].py`)
   - [What it does]
   - [Input/output]
   - [Purpose]

2. **[Stage 2 Name]** (`src/[script_name].py`)
   - [What it does]
   - [Input/output]
   - [Purpose]

[Add more stages as needed]

## Source Code Structure

### Directory Organization

```
src/
├── [core_script_1].py              # [Purpose]
├── [core_script_2].py              # [Purpose]
├── [utility_module].py             # [Purpose]
├── [test_script].py                # [Purpose]
└── debug/                          # Debug tools (development only)
    ├── [debug_script_1].py
    └── [debug_script_2].py
```

### Core Scripts

**[Category Name]:**
- **`[script_name].py`** - [Description of what this script does, its inputs, outputs, and role in the pipeline]

**[Another Category]:**
- **`[script_name].py`** - [Description]

**Supporting Modules:**
- **`[module_name].py`** - [Description of utility functions or shared code]

**Development Tools:**
- **`[tool_name].py`** - [Description of development/debugging tools]

**Test Scripts:**
- **`[test_name].py`** - [Description of test purpose]

### How Components Work Together

1. **[Component 1]** (`[script].py`) → [what it produces/does]
2. **[Component 2]** (`[script].py`) → [what it consumes and produces]
3. **[Component 3]** (`[script].py`) → [final output/result]

[Describe the flow of data and control between components]

## Data Architecture

### [Primary Data Type] Structure

[Describe the main data structure used in your project. Include JSON schema, database schema, or data model as appropriate.]

#### Core Schema

```json
{
  "[entity_name]": {
    "[field_1]": "type/description",
    "[field_2]": "type/description",
    "[nested_object]": {
      "[nested_field]": "type/description"
    }
  }
}
```

[Or use appropriate format for your data type: SQL schema, Python dataclass, etc.]

### [Alternative/Secondary Data Structure]

[If you have multiple data structures, describe them here]

### Data Directory Structure

Data is organized by [organizational principle: type, stage, category, etc.]:

```
data/
├── raw/                          # Source data files
│   └── [source_file]            # Original data
├── processed/                    # Processed/intermediate data
│   └── [processed_file]
├── [category_1]/                 # Category-specific data
│   └── [category_files]
├── [category_2]/                 # Another category
│   └── [category_files]
└── [other_directories]/          # Additional organization
```

**Pipeline Benefits:**
- [Benefit 1 of your organization]
- [Benefit 2]
- [Benefit 3]

**Design Principle**: [Key principle guiding your data organization]

## [Processing Pipeline Name]

### [Stage Name] Approach

**[Stage 1: Name]** (`src/[script].py`)
- [What this stage does]
- [How it processes data]
- [Output format]
- **Purpose**: [Why this stage exists]

**[Stage 2: Name]** (`src/[script].py`)
- [What this stage does]
- [How it processes data]
- [Output format]
- **Purpose**: [Why this stage exists]

[Add more stages as needed]

### [Data Format] Parsing

**[Parsing Method]**: [Describe how you parse your data source]

**Key Patterns Extracted**:
1. **[Pattern Type 1]**: [Description]
2. **[Pattern Type 2]**: [Description]
3. **[Pattern Type 3]**: [Description]

### Extraction/Processing Functions

**Core Processing Scripts**:
- `src/[script].py` - [Purpose]

Key functions:
- `[function_name]()` - [What it does]
- `[function_name]()` - [What it does]
- `[function_name]()` - [What it does]

### Filtering & Quality

- **[Filter Type]**: [Description of filtering logic]
- **[Quality Check]**: [Description of quality assurance]
- **[Validation]**: [Description of validation steps]

## [Core Feature/Functionality]

### [Feature Component 1]

[Description of feature component]

### [Feature Component 2]

[Description of feature component]

### [Feature Strategy/Approach]

[Describe the overall strategy or approach for this feature]

**Quality Metrics**:
- [Metric 1]: [Target/Current value]
- [Metric 2]: [Target/Current value]
- [Metric 3]: [Target/Current value]

## Key Architectural Decisions

### 1. [Decision Name]

**Decision**: [What was decided]

**Rationale**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Alternative Considered**: [What alternative was considered and why it was rejected]

### 2. [Another Decision]

**Decision**: [What was decided]

**Rationale**:
- [Reason 1]
- [Reason 2]

**Alternative Considered**: [Alternative and why rejected]

[Add more key decisions as needed]

## Technical Stack

### Backend Processing
- **Language**: [Python, JavaScript, etc.]
- **Libraries**: [Key libraries used]
- **Data Format**: [JSON, XML, CSV, etc.]
- **Processing**: [Streaming, batch, etc.]

### Frontend (if applicable)
- **Hosting**: [Platform]
- **Language**: [HTML, JavaScript, etc.]
- **Framework**: [if any]
- **Data Loading**: [Method]

### Development Tools
- **Version Control**: [Git, etc.]
- **IDE**: [Cursor, VS Code, etc.]
- **Documentation**: [Markdown, etc.]

## Repository Architecture

### Git Repository Setup

**Repository Strategy**: [Choose one]
- **Standalone Repository**: Project has its own `.git` folder and independent version control
- **Submodule**: Project is tracked as a Git submodule within a parent repository
- **No Version Control**: Project files are managed manually or through parent repository

**If Using Standalone Repository**:
- **Remote Repository**: [GitHub/GitLab URL or "None - local only"]
- **Branch Strategy**: [main/master only, feature branches, git-flow, etc.]
- **Deployment Branch**: [Which branch is deployed to production]

**Important Notes**:
- Projects within Resonance7 framework are excluded from the parent repository (per `.gitignore`)
- Each project can have its own Git repository if needed
- If deploying, ensure the project's `.git` folder is separate from the parent workspace
- Use project-level `.gitignore` to control what gets committed

**Repository Structure**:
```
[project-name]/
├── .git/                    # Project's own Git repository (if using standalone)
├── .gitignore              # Project-specific ignore rules
└── [project files]
```

## Performance Considerations

### Processing Performance
- **Method**: [Streaming, batch, parallel, etc.]
- **Processing Time**: [Expected/actual time]
- **Output Size**: [Size of outputs]

### [Application] Performance
- **Initial Load**: [Load time/size]
- **Future Optimization**: [Planned optimizations]
- **Caching**: [Caching strategy]

### Scalability
- **Current**: [Current capacity]
- **Future**: [Planned scalability improvements]
- **Limitations**: [Known limitations]

## Future Considerations

### Phase [N]: [Feature Name]
- [Planned feature 1]
- [Planned feature 2]
- [Planned feature 3]

### Phase [N+1]: [Another Feature]
- [Planned feature 1]
- [Planned feature 2]

[Add more phases as needed]

## Maintenance & Updates

### Data Updates
- [How data is updated]
- [Update frequency]
- [Version control strategy]

### Code Maintenance
- [What needs maintenance]
- [Update triggers]
- [Testing strategy]

## References

- **[Resource Name]**: [URL or reference]
- **[Another Resource]**: [URL or reference]

---

**Last Updated**: [Date]  
**Status**: [Active Development / Stable / Deprecated]  
**Version**: [Version number]

