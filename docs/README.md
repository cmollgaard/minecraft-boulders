# Minecraft Boulders Datapack

Add terrain-aware boulders to your Minecraft world with this data pack! Boulders naturally scale with terrain height - larger boulders appear in mountainous regions while flat areas remain mostly boulder-free.

## Features

- 🏔️ **Terrain-Aware Generation**: Boulders scale with terrain height using Minecraft's noise patterns
- 🪨 **Three Boulder Sizes**: Small, medium, and large boulders for variety
- 🎲 **Natural Variation**: Multiple stone types (stone, cobblestone, andesite, granite, diorite, mossy cobblestone)
- ⚙️ **Configurable**: Easily adjust spawn rates, sizes, and biome restrictions
- 🌍 **Performance Optimized**: Minimal impact on world generation
- 🔧 **Noise-Based Density**: Uses custom density functions that read terrain patterns

## Requirements

- **Minecraft Version**: Java Edition 1.20+ (pack_format 18)
- **Compatible With**: Most other datapacks and mods
- **Biome Support**: Works in all overworld biomes
- **Multiplayer**: Yes, works on servers

## Installation

1. Download the datapack (or clone this repository)
2. Locate your Minecraft world's `datapacks` folder:
   - **Windows**: `%appdata%\.minecraft\saves\[WorldName]\datapacks`
   - **Mac**: `~/Library/Application Support/minecraft/saves/[WorldName]/datapacks`
   - **Linux**: `~/.minecraft/saves/[WorldName]/datapacks`
3. Copy the `minecraft-boulders` folder (or the repository root) into the `datapacks` folder
4. Start your world or run `/reload` if already in-game
5. Verify installation with `/datapack list` - you should see the boulders datapack listed

## How It Works

### Terrain-Aware Placement

The datapack uses Minecraft's density functions to create terrain-aware boulder generation:

- **Density Functions** (`data/boulders/worldgen/density_function/`): Read terrain height and noise patterns
- **Height-Based Scaling**: 
  - Small boulders spawn at Y=50-160 (lower frequency)
  - Medium boulders spawn at Y=70-180 (moderate frequency)
  - Large boulders spawn at Y=90-200 (higher frequency in mountains)
- **Noise Integration**: Combines terrain noise with boulder placement for natural distribution

### Boulder Types

| Size | Block Count | Height Range | Rarity (1-in-N) |
|------|-------------|--------------|-----------------|
| Small | 2-5 blocks | Y=50-160 | 12 |
| Medium | 6-12 blocks | Y=70-180 | 8 |
| Large | 13-25 blocks | Y=90-200 | 5 |

### Block Composition

Boulders are made from weighted random selection of:
- Stone (most common)
- Cobblestone
- Andesite
- Granite (large boulders)
- Diorite (large boulders)
- Mossy Cobblestone (rare)

## Quick Start Configuration

For detailed configuration options, see [CONFIGURATION.md](CONFIGURATION.md).

### Adjusting Spawn Frequency

Edit the `rarity_filter` values in `data/boulders/worldgen/placed_feature/*.json`:
- Lower values = more common (e.g., `"chance": 3` for very common)
- Higher values = more rare (e.g., `"chance": 20` for very rare)

### Changing Height Ranges

Modify the `height_range` in placed feature files to control where boulders spawn.

## Troubleshooting

### Boulders not spawning

1. Verify datapack is enabled: `/datapack list`
2. Check that you're exploring new chunks (boulders only generate in newly created terrain)
3. Make sure you're in appropriate height range (Y=50-200)
4. Run `/reload` after making configuration changes

### Too many/few boulders

Adjust the `rarity_filter` chance values in the placed feature files. Reload with `/reload` after changes.

### Performance issues

Reduce the `tries` value in configured feature files to place fewer blocks per boulder.

## Documentation

- [Configuration Guide](CONFIGURATION.md) - Detailed configuration options
- [Technical Documentation](TECHNICAL.md) - Technical details about noise patterns and implementation
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to this project

## License

This project is open source under the MIT License. See [LICENSE](../LICENSE) file for details.

## Credits

Created using Minecraft's worldgen system and density functions. Inspired by natural boulder formations found in real-world mountainous terrain.

## External Resources

- [Minecraft Wiki - Custom World Generation](https://minecraft.wiki/w/Custom_world_generation)
- [Minecraft Wiki - Density Functions](https://minecraft.wiki/w/Density_function)
- [Misode's Worldgen Generators](https://misode.github.io/) - Visual tools for datapack generation
