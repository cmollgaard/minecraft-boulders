# Minecraft Boulders Datapack - Agent Instructions

## Project Overview

This project creates a Minecraft datapack that adds configurable boulders to the Minecraft world using noise patterns that integrate with Minecraft's terrain generation system. The boulders scale with terrain height - they appear larger in mountainous/tall terrain and smaller or non-existent in flat areas.

## Project Goals

1. **Terrain-Aware Boulder Generation**: Create boulders that respond to Minecraft's existing noise patterns for terrain generation
2. **Adaptive Scaling**: Large boulders in tall/mountainous terrain, small or absent boulders in flat terrain
3. **Configurable System**: Allow users to configure boulder appearance, frequency, and behavior
4. **Natural Integration**: Boulders should feel like a natural part of the Minecraft world generation

## Technical Approach

### Core Components

1. **Datapack Structure** (`data/boulders/`)
   - Configured features for boulder block patterns
   - Placed features for boulder placement rules
   - Density functions that read terrain noise values
   - Optional noise settings modifications

2. **Noise-Based Placement**
   - Use Minecraft's built-in density functions to read terrain height
   - Create custom density functions that combine terrain noise with boulder generation
   - Scale boulder size and frequency based on terrain noise values

3. **Feature Types**
   - Small boulders (2-5 blocks) for moderate terrain
   - Medium boulders (6-12 blocks) for hilly terrain  
   - Large boulders (13-25 blocks) for mountainous terrain
   - Rare massive boulders (25+ blocks) for extreme peaks

## Architecture

```
minecraft-boulders/
├── pack.mcmeta                          # Datapack metadata
├── data/
│   └── boulders/
│       ├── worldgen/
│       │   ├── configured_feature/      # Boulder block patterns
│       │   │   ├── small_boulder.json
│       │   │   ├── medium_boulder.json
│       │   │   └── large_boulder.json
│       │   ├── placed_feature/          # Placement rules
│       │   │   ├── small_boulder.json
│       │   │   ├── medium_boulder.json
│       │   │   └── large_boulder.json
│       │   └── density_function/        # Terrain-aware density
│       │       ├── boulder_density.json
│       │       └── terrain_height.json
│       └── tags/
│           └── worldgen/
│               └── biome/               # Biome filters (optional)
│                   └── has_boulders.json
```

## Implementation Guidelines

### For Code Agents

1. **File Format**: All worldgen files are JSON format following Minecraft 1.20+ specifications
2. **Naming Convention**: Use lowercase with underscores (e.g., `small_boulder.json`)
3. **Namespace**: Use `boulders` as the primary namespace for all features
4. **Pack Format**: Target pack_format 18+ for Minecraft 1.20+
5. **Testing**: Datapack should be testable by placing in `world/datapacks/` folder

### For Documentation Agents

1. **User Guide**: Create clear documentation for end-users
2. **Configuration Examples**: Provide examples of customizing boulder generation
3. **Installation Instructions**: Step-by-step installation guide
4. **Troubleshooting**: Common issues and solutions

### For Testing Agents

1. **Structure Validation**: Verify JSON syntax and datapack structure
2. **Game Testing**: Test in actual Minecraft world generation
3. **Edge Cases**: Test in various biomes and terrain types
4. **Performance**: Ensure boulder generation doesn't cause lag

## Key Technical Details

### Density Functions

Density functions allow reading Minecraft's terrain noise patterns:
- Use `minecraft:y_clamped_gradient` to detect terrain height
- Combine with noise functions to add randomization
- Use `minecraft:mul` to scale boulder probability with terrain height

### Configured Features

Boulders use `minecraft:random_patch` or `minecraft:simple_block` features:
- Define block placement patterns
- Use probability and spread for natural appearance
- Support multiple block types (stone, cobblestone, andesite, etc.)

### Placed Features

Control where configured features spawn:
- Use height range filters
- Apply biome restrictions
- Set spawn probability
- Add noise-based threshold filters

## Configuration Options

Users should be able to configure:
1. **Boulder frequency**: How often boulders spawn
2. **Size variation**: Min/max boulder sizes
3. **Block types**: Which stones are used
4. **Biome restrictions**: Where boulders can appear
5. **Height thresholds**: Minimum terrain height for boulder spawning

## Success Criteria

- ✅ Datapack loads without errors in Minecraft
- ✅ Boulders spawn in appropriate terrain
- ✅ Boulder size correlates with terrain height
- ✅ Flat areas have few or no boulders
- ✅ Mountain areas have larger, more frequent boulders
- ✅ Performance impact is negligible
- ✅ Documentation is clear and complete

## Development Workflow

1. Create basic datapack structure with pack.mcmeta
2. Implement simple configured feature for small boulders
3. Add placed feature with basic height restrictions
4. Create density functions that read terrain noise
5. Integrate density functions with placed features
6. Add multiple boulder sizes
7. Test in various biomes and terrain types
8. Document configuration options
9. Create user guide and examples

## References

- [Minecraft Wiki - Custom World Generation](https://minecraft.wiki/w/Custom_world_generation)
- [Minecraft Wiki - Density Functions](https://minecraft.wiki/w/Density_function)
- [Minecraft Wiki - Configured Features](https://minecraft.wiki/w/Configured_feature)
- [Misode's Worldgen Generators](https://misode.github.io/)

## Notes for Agents

- Always validate JSON syntax before committing
- Test changes in actual Minecraft when possible
- Keep backward compatibility in mind
- Document any breaking changes
- Follow Minecraft's naming conventions
- Use vanilla Minecraft block types for compatibility
- Optimize for performance - worldgen runs for every chunk
