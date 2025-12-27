# AGENTS.explainer.md

This document explains how to set up and maintain the `AGENTS.md` file for this project. The goal is to create a living document that captures all project requirements, enabling any agent to recreate the project from scratch using only the information in `AGENTS.md`.

## Purpose of AGENTS.md

The `AGENTS.md` file serves as the single source of truth for project requirements. It should contain:

- **Project Overview**: What the project does and its core purpose
- **Technical Requirements**: Technologies, frameworks, and specifications needed
- **Feature Requirements**: Detailed descriptions of all features
- **Architecture Decisions**: Key design choices and their rationale
- **Implementation Guidelines**: How features should be built
- **Testing Requirements**: What needs to be tested and how
- **Deployment/Usage Instructions**: How to build, package, and use the project

## AGENTS.md Structure

The `AGENTS.md` file should follow this structure:

```markdown
# Project: [Project Name]

## Overview
[Brief description of what the project does]

## Core Requirements
- [Requirement 1]
- [Requirement 2]
- [...]

## Technical Specifications
### Platform/Framework
[Details about the target platform, frameworks used, etc.]

### File Structure
[Expected project structure]

### Dependencies
[Any external dependencies]

## Features
### Feature 1: [Name]
- **Description**: [What the feature does]
- **Implementation**: [How it should be implemented]
- **Acceptance Criteria**: [How to verify it works]

### Feature 2: [Name]
[...]

## Architecture Decisions
### Decision 1: [Title]
- **Context**: [Why this decision was needed]
- **Decision**: [What was decided]
- **Rationale**: [Why this choice was made]

## Testing
[How to test the project]

## Build & Deployment
[How to build and deploy/use the project]

## Changelog
[Track major changes to requirements over time]
```

## Guidelines for Maintaining AGENTS.md

### Adding New Requirements

When new requirements are introduced:

1. **Document immediately**: Add new requirements as soon as they are identified
2. **Be specific**: Include enough detail that another agent could implement without ambiguity
3. **Include context**: Explain why the requirement exists, not just what it is
4. **Link related items**: Reference related features or decisions when applicable

### Refining Existing Requirements

As the project evolves:

1. **Keep it current**: Update requirements when implementation details change
2. **Don't delete history**: Use strikethrough or move to a "deprecated" section rather than deleting
3. **Version changes**: Note when requirements were modified in the changelog
4. **Resolve conflicts**: If requirements conflict, document the resolution

#### Example: Handling Deprecated Requirements

Use strikethrough for inline deprecation:
```markdown
- ~~Boulders spawn in all biomes~~ → Boulders spawn only in mountain and forest biomes (changed v1.2)
```

Or create a dedicated deprecated section:
```markdown
## Deprecated Requirements
### Boulder Size Variants (deprecated v1.3)
- **Original**: Support small, medium, and large boulder sizes
- **Replaced by**: Dynamic size based on biome elevation
- **Reason**: Simplified implementation, more natural appearance
```

### Best Practices

1. **Completeness**: The file should contain everything needed to recreate the project
2. **Clarity**: Use clear, unambiguous language
3. **Organization**: Keep related information grouped together
4. **Testability**: Requirements should be verifiable
5. **Independence**: Requirements should be understandable without external context

## Example: This Project (minecraft-boulders)

For this Minecraft data pack project, an `AGENTS.md` might include:

- **Overview**: A Minecraft data pack that adds boulder terrain features to world generation
- **Technical Specs**: Minecraft data pack format, target Minecraft version, pack format version
- **Features**: Types of boulders, generation rules, biome restrictions, etc.
- **Architecture**: File structure for data packs, function organization
- **Testing**: How to test in Minecraft (world creation, commands, etc.)
- **Build**: How to package the data pack for distribution

## The Recreate Test

The ultimate test of a good `AGENTS.md` is the "Recreate Test":

> If you gave only the `AGENTS.md` file to a new agent with no prior knowledge of the project, could they recreate the entire project correctly?

If the answer is yes, the `AGENTS.md` is comprehensive enough. If not, identify what's missing and add it.

## Continuous Improvement

The `AGENTS.md` file should grow and improve over time:

1. After completing a feature, ensure `AGENTS.md` reflects the final implementation
2. When discovering edge cases, document them as requirements
3. When making architectural decisions, record them immediately
4. Regularly review for clarity and completeness
5. Update when project dependencies or tooling changes
