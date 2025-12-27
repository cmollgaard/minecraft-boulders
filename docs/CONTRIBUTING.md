# Contributing Guide

Thank you for your interest in contributing to the Minecraft Boulders datapack! This guide explains how to contribute effectively.

## Ways to Contribute

- 🐛 **Report bugs or issues**
- 💡 **Suggest new features**
- 📝 **Submit pull requests**
- 📖 **Improve documentation**
- 🎨 **Share custom configurations**
- 🧪 **Test and provide feedback**

## Getting Started

### Prerequisites

- Minecraft Java Edition 1.20+
- Basic understanding of JSON syntax
- Familiarity with Minecraft datapacks (helpful but not required)

### Setting Up

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/minecraft-boulders.git
   ```
3. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### File Structure

Maintain the standard Minecraft datapack structure:

```
data/boulders/worldgen/
├── configured_feature/   # What boulders look like
├── placed_feature/       # Where boulders spawn
└── density_function/     # Terrain-aware placement logic
```

### Naming Conventions

- Use lowercase with underscores for file names: `my_feature.json`
- Namespace all features with `boulders:` prefix
- Use descriptive names: `large_boulder.json` not `lb.json`

### JSON Style

- Use 2-space indentation
- Keep entries in consistent order
- Validate JSON syntax before committing
- Test changes in Minecraft before submitting

### Testing Your Changes

1. Copy the datapack to a test world's `datapacks` folder
2. Run `/reload` in-game
3. Generate new chunks to see your changes
4. Test across different biomes and elevations
5. Verify no errors appear in the game log

### Validation

Before submitting, ensure:

- [ ] All JSON files are valid (use `python3 -m json.tool filename.json`)
- [ ] Changes work in Minecraft 1.20+
- [ ] No breaking changes to existing features (unless intentional)
- [ ] Documentation is updated if needed

## Submitting Changes

### Pull Request Process

1. Ensure your branch is up to date with main
2. Write clear commit messages describing your changes
3. Submit a pull request with:
   - Clear description of what changes
   - Why the changes are needed
   - How you tested the changes
4. Wait for review and address any feedback

### Commit Messages

Use clear, descriptive commit messages:

```
Good: Add granite blocks to large boulder composition
Bad: Update files
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Testing
How did you test this change?

## Screenshots (if applicable)
Include screenshots showing the change in-game
```

## Code of Conduct

- Be respectful and constructive
- Help others learn
- Focus on improving the project
- Credit others' contributions

## Questions?

If you have questions about contributing:

- Open a GitHub issue for discussion
- Check existing issues for similar questions
- Review the [Technical Documentation](TECHNICAL.md) for implementation details

## Recognition

Contributors will be acknowledged in the project. Thank you for helping improve the Minecraft Boulders datapack!
