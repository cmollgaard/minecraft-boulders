# Configuration Guide

This guide explains how to customize boulder generation by editing the JSON files in the datapack.

## File Structure

The configuration files are organized as follows:

```
data/boulders/worldgen/
├── configured_feature/           # Boulder block patterns
│   ├── small_boulder.json       # Small boulder configuration
│   ├── medium_boulder.json      # Medium boulder configuration
│   └── large_boulder.json       # Large boulder configuration
├── placed_feature/               # Placement rules
│   ├── small_boulder.json       # Where small boulders spawn
│   ├── medium_boulder.json      # Where medium boulders spawn
│   └── large_boulder.json       # Where large boulders spawn
└── density_function/             # Terrain-aware density
    ├── terrain_height_factor.json
    └── boulder_density.json
```

## Adjusting Spawn Frequency

Edit the `rarity_filter` values in `data/boulders/worldgen/placed_feature/*.json`:

- **Lower values** = more common (e.g., `"chance": 3` for very common)
- **Higher values** = more rare (e.g., `"chance": 20` for very rare)

### Example: Make small boulders more common

In `placed_feature/small_boulder.json`, change:
```json
{
  "type": "minecraft:rarity_filter",
  "chance": 6
}
```

### Current Default Values

| Boulder Size | Rarity Chance | Spawn Rate |
|-------------|---------------|------------|
| Small | 12 | 1-in-12 chunks |
| Medium | 8 | 1-in-8 chunks |
| Large | 5 | 1-in-5 chunks |

## Changing Height Ranges

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

### Current Default Height Ranges

| Boulder Size | Min Height | Max Height |
|-------------|------------|------------|
| Small | Y=50 | Y=160 |
| Medium | Y=70 | Y=180 |
| Large | Y=90 | Y=200 |

The overlapping ranges create natural transition zones where multiple boulder sizes can appear.

## Modifying Boulder Size

Edit the `tries`, `xz_spread`, and `y_spread` values in configured feature files:

| Parameter | Description | Effect |
|-----------|-------------|--------|
| `tries` | Number of blocks to place | More = larger boulder |
| `xz_spread` | Horizontal spread | Larger = wider boulder |
| `y_spread` | Vertical spread | Larger = taller boulder |

### Current Default Values

| Boulder Size | tries | xz_spread | y_spread |
|-------------|-------|-----------|----------|
| Small | 3 | 2 | 1 |
| Medium | 6 | 3 | 2 |
| Large | 12 | 4 | 3 |

### Example: Make large boulders bigger

In `configured_feature/large_boulder.json`, change:
```json
{
  "type": "minecraft:random_patch",
  "config": {
    "tries": 20,
    "xz_spread": 6,
    "y_spread": 4,
    ...
  }
}
```

## Changing Block Types

Modify the `weighted_state_provider` entries in configured feature files:

```json
{
  "weight": 5,
  "data": {
    "Name": "minecraft:stone"
  }
}
```

### Current Block Weights

**Small and Medium Boulders:**
| Block | Weight |
|-------|--------|
| stone | 4-5 |
| cobblestone | 3 |
| andesite | 2 |
| mossy_cobblestone | 1 |

**Large Boulders:**
| Block | Weight |
|-------|--------|
| stone | 6 |
| cobblestone | 3 |
| andesite | 2 |
| diorite | 1 |
| granite | 1 |

### Example: Add deepslate to boulders

In any configured feature file, add to the `entries` array:
```json
{
  "weight": 2,
  "data": {
    "Name": "minecraft:deepslate"
  }
}
```

## Density Function Configuration

The density functions control terrain-aware placement:

### terrain_height_factor.json

Controls how boulder density scales with height:
- Uses `y_clamped_gradient` from Y=60 to Y=200
- Values range from -0.5 (low terrain) to 1.0 (high terrain)

### boulder_density.json

Combines height factor with noise for natural distribution:
- Multiplies terrain height factor with calcite noise
- Creates clustered, natural-looking boulder placement

## Tips

1. **Test incrementally**: Make one change at a time and test with `/reload`
2. **Explore new chunks**: Changes only affect newly generated terrain
3. **Backup your files**: Save original files before making changes
4. **Use JSON validators**: Syntax errors will prevent the datapack from loading
5. **Balance changes**: More boulders may impact performance

## Applying Changes

After editing any configuration file:

1. Save the file
2. Run `/reload` in Minecraft
3. Explore new chunks to see the changes

Note: Existing chunks are not affected by configuration changes.
