# Minecraft Boulders Datapack

Add terrain-aware boulders to your Minecraft world with this data pack! Boulders naturally scale with terrain height - larger boulders appear in mountainous regions while flat areas remain mostly boulder-free.

## Features

- 🏔️ **Terrain-Aware Generation**: Boulders scale with terrain height using Minecraft's noise patterns
- 🪨 **Three Boulder Sizes**: Small, medium, and large boulders for variety
- 🎲 **Natural Variation**: Multiple stone types (stone, cobblestone, andesite, granite, diorite, mossy cobblestone)
- ⚙️ **Configurable**: Easily adjust spawn rates, sizes, and biome restrictions
- 🌍 **Performance Optimized**: Minimal impact on world generation
- 🔧 **Noise-Based Density**: Uses custom density functions that read terrain patterns

## Installation

1. Download the datapack (or clone this repository)
2. Locate your Minecraft world's `datapacks` folder:
   - Windows: `%appdata%\.minecraft\saves\[WorldName]\datapacks`
   - Mac: `~/Library/Application Support/minecraft/saves/[WorldName]/datapacks`
   - Linux: `~/.minecraft/saves/[WorldName]/datapacks`
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

- **Small Boulders**: 2-5 blocks, rare, found in moderate terrain
- **Medium Boulders**: 6-12 blocks, common in hills and slopes
- **Large Boulders**: 13-25 blocks, frequent in mountainous areas

### Block Composition

Boulders are made from weighted random selection of:
- Stone (most common)
- Cobblestone
- Andesite
- Granite (large boulders)
- Diorite (large boulders)
- Mossy Cobblestone (rare)

## Configuration

You can customize boulder generation by editing the JSON files:

### Adjusting Spawn Frequency

Edit the `rarity_filter` values in `data/boulders/worldgen/placed_feature/*.json`:
- Lower values = more common (e.g., `"chance": 3` for very common)
- Higher values = more rare (e.g., `"chance": 20` for very rare)

Example (make small boulders more common):
```json
{
  "type": "minecraft:rarity_filter",
  "chance": 6
}
```

### Changing Height Ranges

Modify the `height_range` in placed feature files to control where boulders spawn:
```json
{
  "type": "minecraft:height_range",
  "height": {
    "type": "minecraft:uniform",
    "min_inclusive": {"absolute": 50},
    "max_inclusive": {"absolute": 200}
  }
}
```

### Modifying Boulder Size

Edit the `tries`, `xz_spread`, and `y_spread` values in configured feature files:
- `tries`: Number of blocks to place (more = larger boulder)
- `xz_spread`: Horizontal spread (larger = wider boulder)
- `y_spread`: Vertical spread (larger = taller boulder)

### Changing Block Types

Modify the `weighted_state_provider` entries in configured feature files:
```json
{
  "weight": 5,
  "data": {
    "Name": "minecraft:stone"
  }
}
```

## Technical Details

### Datapack Structure

```
minecraft-boulders/
├── pack.mcmeta                               # Datapack metadata (format 18)
├── AGENTS.md                                 # Agent instructions
├── README.md                                 # This file
└── data/
    └── boulders/
        └── worldgen/
            ├── configured_feature/           # Boulder block patterns
            │   ├── small_boulder.json
            │   ├── medium_boulder.json
            │   └── large_boulder.json
            ├── placed_feature/               # Placement rules
            │   ├── small_boulder.json
            │   ├── medium_boulder.json
            │   └── large_boulder.json
            └── density_function/             # Terrain-aware density
                ├── terrain_height_factor.json
                └── boulder_density.json
```

### Density Functions

The datapack includes custom density functions that integrate with Minecraft's terrain generation:

- **terrain_height_factor.json**: Maps terrain height (Y 60-200) to boulder probability
- **boulder_density.json**: Combines height factor with noise for natural distribution

These functions ensure boulders scale appropriately with terrain - more and larger boulders in mountains, fewer in plains.

## Compatibility

- **Minecraft Version**: 1.20+ (pack_format 15-18)
- **Compatible With**: Most other datapacks and mods
- **Biome Support**: Works in all overworld biomes
- **Multiplayer**: Yes, works on servers

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

## Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest new features
- Submit pull requests
- Share your custom configurations

## License

This project is open source. See LICENSE file for details.

## Credits

Created using Minecraft's worldgen system and density functions. Inspired by natural boulder formations found in real-world mountainous terrain.

## See Also

- [AGENTS.md](AGENTS.md) - Technical implementation details and agent instructions
- [Minecraft Wiki - Custom World Generation](https://minecraft.wiki/w/Custom_world_generation)
- [Minecraft Wiki - Density Functions](https://minecraft.wiki/w/Density_function)
