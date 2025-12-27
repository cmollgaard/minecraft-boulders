# Project: Minecraft Boulders Datapack

## Overview

This project creates a Minecraft datapack that adds configurable, terrain-aware boulders to the Minecraft world. Boulders are generated using noise patterns that integrate with Minecraft's terrain generation system, scaling with terrain height - they appear larger and more frequent in mountainous/tall terrain and smaller or non-existent in flat areas.

## Core Requirements

- Create a valid Minecraft datapack compatible with Minecraft 1.20+ (pack_format 15-18)
- Implement terrain-aware boulder generation that responds to Minecraft's noise patterns
- Boulders must scale with terrain height: large in mountains, small in hills, minimal in flat areas
- Support multiple boulder sizes with natural variation
- Use only vanilla Minecraft blocks for compatibility
- Minimal performance impact on world generation
- Provide user-configurable options for spawn rates and appearance
- Include comprehensive documentation for installation and configuration

## Technical Specifications

### Platform/Framework

- **Platform**: Minecraft Java Edition 1.20+
- **Format**: Data Pack (pack_format 18, with fallback support for 15-17)
- **Language**: JSON configuration files
- **Namespace**: `boulders`
- **Note**: While pack.mcmeta declares support for formats 15-18, the density functions and worldgen features used are optimized for Minecraft 1.20+ (format 18). Earlier versions may have limited or no functionality.

### File Structure

```
minecraft-boulders/
├── pack.mcmeta                          # Datapack metadata (pack_format 18)
├── AGENTS.md                            # This file - project requirements
├── README.md                            # User documentation
├── LICENSE                              # License file
└── data/
    └── boulders/                        # Main namespace
        └── worldgen/
            ├── configured_feature/      # Boulder block patterns
            │   ├── small_boulder.json   # 2-5 blocks (tries: 3, xz_spread: 2)
            │   ├── medium_boulder.json  # 6-12 blocks (tries: 6, xz_spread: 3)
            │   └── large_boulder.json   # 13-25 blocks (tries: 12, xz_spread: 4)
            ├── placed_feature/          # Placement rules with height-based spawning
            │   ├── small_boulder.json   # Y=50-160, rarity chance: 12 (1-in-12)
            │   ├── medium_boulder.json  # Y=70-180, rarity chance: 8 (1-in-8)
            │   └── large_boulder.json   # Y=90-200, rarity chance: 5 (1-in-5)
            └── density_function/        # Terrain-aware distribution
                ├── terrain_height_factor.json  # Y-gradient (60-200)
                └── boulder_density.json        # Noise + height factor
```

### Dependencies

- Minecraft Java Edition 1.20 or later
- No external mods or dependencies required
- Uses only vanilla Minecraft worldgen features


## Features

### Feature 1: Terrain-Aware Boulder Generation
- **Description**: Boulders that automatically scale with terrain height using Minecraft's native noise patterns
- **Implementation**: 
  - Use `minecraft:y_clamped_gradient` density function to read terrain height (Y=60-200)
  - Combine with `minecraft:noise` using calcite noise for natural randomization
  - Scale boulder size and frequency based on calculated density values
- **Acceptance Criteria**:
  - Boulders spawn more frequently at higher elevations
  - Large boulders only appear in mountainous terrain (Y>90)
  - Flat areas (Y<70) have minimal or no boulder generation
  - Boulder distribution looks natural and varied

### Feature 2: Multiple Boulder Sizes
- **Description**: Three distinct boulder size variants for terrain variety
- **Implementation**:
  - **Small Boulder**: `random_patch` with tries=3, xz_spread=2, y_spread=1
  - **Medium Boulder**: `random_patch` with tries=6, xz_spread=3, y_spread=2
  - **Large Boulder**: `random_patch` with tries=12, xz_spread=4, y_spread=3
  - Each uses `simple_block` feature with weighted stone variants
- **Acceptance Criteria**:
  - Small boulders: 2-5 blocks, spawn at Y=50-160
  - Medium boulders: 6-12 blocks, spawn at Y=70-180
  - Large boulders: 13-25 blocks, spawn at Y=90-200
  - Size distribution correlates with terrain height

### Feature 3: Natural Block Variation
- **Description**: Boulders use multiple stone types for natural appearance
- **Implementation**:
  - Use `minecraft:weighted_state_provider` for block selection
  - Block types: stone (most common), cobblestone, andesite, granite, diorite, mossy cobblestone
  - Weight distribution favors stone with variety from other types
- **Acceptance Criteria**:
  - Boulders contain mix of stone types
  - Stone is most common block type
  - Variation appears natural and not overly patterned
  - All blocks are vanilla Minecraft blocks

### Feature 4: Height-Based Placement Control
- **Description**: Boulders spawn only within appropriate height ranges with environment scanning
- **Implementation**:
  - Use `minecraft:height_range` with `uniform` distribution
  - Use `minecraft:environment_scan` to find solid ground (max 32 steps down)
  - Use `minecraft:rarity_filter` for spawn frequency control
  - Use `minecraft:in_square` for chunk-based distribution
- **Acceptance Criteria**:
  - Boulders always spawn on solid ground
  - No floating boulders in air
  - No boulders underground
  - Spawn rates increase with elevation

### Feature 5: User Configuration
- **Description**: Allow users to customize boulder generation through JSON editing
- **Implementation**:
  - Document configuration options in README.md
  - Provide examples for common adjustments
  - Clear structure for editing spawn rates, sizes, and block types
- **Acceptance Criteria**:
  - Users can adjust spawn frequency via `rarity_filter` chance values
  - Users can modify height ranges in placed features
  - Users can change block types in configured features
  - Users can adjust boulder sizes via tries and spread values
  - Documentation clearly explains each configuration option

### Feature 6: Cross-Chunk Generation
- **Description**: Boulders can span multiple chunks naturally
- **Implementation**:
  - Use `xz_spread` values (2-4) that allow placement across chunk boundaries
  - Rely on Minecraft's native chunk generation for seamless integration
- **Acceptance Criteria**:
  - Boulders placed near chunk edges extend into neighboring chunks
  - No artificial constraints at chunk boundaries (16x16 blocks)
  - Generation looks continuous across chunks

## Architecture Decisions

### Decision 1: Use random_patch Instead of Large Structure Features
- **Context**: Need to generate scattered boulders of varying sizes across terrain
- **Decision**: Use `minecraft:random_patch` with nested `simple_block` features
- **Rationale**: 
  - Simpler implementation than custom structures
  - Better performance for small scattered features
  - Native integration with worldgen placement modifiers
  - Easier for users to configure and understand

### Decision 2: Density Functions for Terrain Awareness
- **Context**: Boulders must scale with terrain height following Minecraft's noise patterns
- **Decision**: Create custom density functions that read Y-gradient and combine with noise
- **Rationale**:
  - Integrates with Minecraft's existing terrain generation
  - Provides smooth scaling rather than hard cutoffs
  - Uses native worldgen systems for performance
  - Follows Minecraft's architectural patterns

### Decision 3: Three Size Tiers
- **Context**: Need variety in boulder sizes without overcomplicating system
- **Decision**: Implement exactly three sizes (small, medium, large) with distinct height ranges
- **Rationale**:
  - Sufficient variety for natural appearance
  - Clear progression with terrain height
  - Simple to configure and understand
  - Manageable number of JSON files

### Decision 4: Height-Stratified Placement
- **Context**: Boulder size must correlate with terrain elevation
- **Decision**: Use overlapping but offset height ranges (small: 50-160, medium: 70-180, large: 90-200)
- **Rationale**:
  - Creates natural transition zones between sizes
  - Higher elevations have access to all sizes but favor larger
  - Lower elevations limited to smaller boulders
  - Avoids artificial size boundaries

### Decision 5: Vanilla Blocks Only
- **Context**: Maximum compatibility and ease of use
- **Decision**: Use only vanilla Minecraft stone block types
- **Rationale**:
  - No mod dependencies required
  - Works in any Minecraft world
  - Familiar blocks for all players
  - Ensures datapack can be shared widely

## Testing

### JSON Validation
- All JSON files must be valid and parse correctly
- Use `python3 -m json.tool` to validate each file
- Verify pack.mcmeta has correct pack_format and description

### Structure Validation
- Verify all required directories exist under `data/boulders/worldgen/`
- Confirm file naming follows lowercase_with_underscores convention
- Check that namespace `boulders` is used consistently

### In-Game Testing
1. **Installation Test**: 
   - Copy datapack to `world/datapacks/` folder
   - Run `/reload` command
   - Verify with `/datapack list` that "boulders" appears

2. **Generation Test**:
   - Create new chunks in various terrain types
   - Confirm boulders spawn in appropriate locations
   - Check mountains (Y>90) for large boulders
   - Check hills (Y=70-90) for medium boulders
   - Check flat areas (Y<70) for minimal spawns

3. **Size Test**:
   - Count blocks in several boulders of each size
   - Verify small: ~2-5 blocks, medium: ~6-12 blocks, large: ~13-25 blocks
   - Confirm size correlates with terrain height

4. **Block Type Test**:
   - Examine boulder composition
   - Confirm mix of stone, cobblestone, andesite, etc.
   - Verify stone is most common

5. **Performance Test**:
   - Generate large number of new chunks
   - Monitor for lag or generation slowdowns
   - Verify boulder generation doesn't significantly impact performance

### Edge Cases
- Test at world height limits (Y=50 and Y=200)
- Test at chunk boundaries
- Test in various biomes (plains, mountains, forests, etc.)
- Test in ocean/water biomes
- Test with other datapacks installed

## Build & Deployment

### Building the Datapack
1. Ensure all files are in correct directory structure
2. Validate all JSON files for syntax errors
3. Test in a Minecraft world
4. Package by creating a ZIP of the entire directory (or use as-is)

### Installation
1. Locate Minecraft world save folder:
   - Windows: `%appdata%\.minecraft\saves\[WorldName]\datapacks`
   - Mac: `~/Library/Application Support/minecraft/saves\[WorldName]/datapacks`
   - Linux: `~/.minecraft/saves/[WorldName]/datapacks`
2. Copy minecraft-boulders folder into datapacks directory
3. Start world or run `/reload` if already running
4. Verify with `/datapack list`

### Usage
- Boulders generate automatically in new chunks
- Existing chunks are not affected (requires new terrain generation)
- Configuration changes require `/reload` command
- Remove datapack and `/reload` to disable

## Implementation Notes

### File Format Specifications
- All worldgen files are JSON format
- Use lowercase with underscores for file names (e.g., `small_boulder.json`)
- Namespace all features with `boulders:` prefix
- Follow Minecraft 1.20+ worldgen JSON schema

### Key JSON Structures

**Configured Feature Format**:
```json
{
  "type": "minecraft:random_patch",
  "config": {
    "tries": <number>,
    "xz_spread": <number>,
    "y_spread": <number>,
    "feature": {
      "feature": {
        "type": "minecraft:simple_block",
        "config": {
          "to_place": {
            "type": "minecraft:weighted_state_provider",
            "entries": [...]
          }
        }
      },
      "placement": []
    }
  }
}
```

**Placed Feature Format**:
```json
{
  "feature": "boulders:<feature_name>",
  "placement": [
    {"type": "minecraft:rarity_filter", "chance": <number>},
    {"type": "minecraft:in_square"},
    {"type": "minecraft:height_range", "height": {...}},
    {"type": "minecraft:environment_scan", ...},
    {"type": "minecraft:random_offset", ...},
    {"type": "minecraft:biome"}
  ]
}
```

**Density Function Format**:
```json
{
  "type": "minecraft:mul|add|max|y_clamped_gradient|noise",
  "argument1": {...},
  "argument2": {...}
}
```

### Performance Considerations
- Keep `tries` values reasonable (3-12 range)
- Use `rarity_filter` to control spawn frequency
- Boulder generation is per-chunk, so optimize for chunk-scale operations
- Density functions are evaluated during worldgen - keep them simple

### Compatibility Notes
- Pack format 18 targets Minecraft 1.20+
- Supports formats 15-18 for broader compatibility
- No mod dependencies - pure vanilla datapack
- Compatible with other datapacks that don't modify terrain generation
- May conflict with datapacks that heavily modify worldgen noise

## Changelog

### v1.0 (Initial Implementation)
- Created datapack structure with pack.mcmeta (pack_format 18)
- Implemented three boulder sizes (small, medium, large)
- Added density functions for terrain-aware placement
- Created configured features with weighted block types
- Implemented placed features with height-stratified spawning
- Added comprehensive README documentation
- Added AGENTS.md for project requirements

## References

- [Minecraft Wiki - Custom World Generation](https://minecraft.wiki/w/Custom_world_generation)
- [Minecraft Wiki - Density Functions](https://minecraft.wiki/w/Density_function)
- [Minecraft Wiki - Configured Features](https://minecraft.wiki/w/Configured_feature)
- [Minecraft Wiki - Data Pack](https://minecraft.wiki/w/Data_pack)
- [Misode's Worldgen Generators](https://misode.github.io/) - Visual tools for datapack generation

## Notes for Agents

### Code Agents
- Always validate JSON syntax before committing
- Follow Minecraft's naming conventions (lowercase with underscores)
- Use vanilla Minecraft block types only
- Test changes in actual Minecraft when possible
- Optimize for performance - worldgen runs for every chunk

### Documentation Agents  
- Keep README.md user-focused with clear installation instructions
- Provide configuration examples for common use cases
- Include troubleshooting section for common issues
- Update documentation when features change

### Testing Agents
- Verify JSON structure and syntax for all files
- Test in actual Minecraft world generation
- Check edge cases (height limits, chunk boundaries, various biomes)
- Monitor performance impact during testing
- Test with and without other datapacks

### Important Constraints
- Keep backward compatibility when making changes
- Document any breaking changes in changelog
- Preserve file structure unless necessary to change
- Maintain consistent naming conventions throughout
