# Extending Minecraft Noise Pattern Terrain Generation (Java Edition)

This guide explains how to extend Minecraft Java Edition's existing terrain generation with custom features that integrate with the world's noise patterns. This is a practical guide focused on **how to extend** the system, not on how the underlying noise system works.

> **⚠️ Java Edition Only**: This guide is specifically for Minecraft Java Edition (1.18+) using datapacks. For Bedrock Edition information, see the [Bedrock Edition section](#bedrock-edition-differences) below.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Bedrock Edition Differences](#bedrock-edition-differences)
3. [Extension Approaches](#extension-approaches)
4. [Approach 1: Using Noise in Placed Features](#approach-1-using-noise-in-placed-features)
5. [Approach 2: Custom Density Functions](#approach-2-custom-density-functions)
6. [Practical Example: Terrain-Aware Boulders](#practical-example-terrain-aware-boulders)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)
9. [Useful Tools](#useful-tools)

## Prerequisites

Before extending Minecraft's noise patterns, you should have:

- A working Minecraft datapack structure with `pack.mcmeta`
- Basic understanding of datapack file organization
- Familiarity with JSON syntax
- Minecraft Java Edition 1.18+ (when the new worldgen system was introduced)

## Bedrock Edition Differences

### Does This Work for Bedrock Edition?

**No, this guide is Java Edition specific.** Bedrock Edition uses a completely different system for terrain customization.

### Key Differences

| Feature | Java Edition | Bedrock Edition |
|---------|--------------|-----------------|
| **Customization Method** | Datapacks with JSON worldgen files | Add-ons with JSON + scripts |
| **Noise Access** | Full control over density functions and noise parameters | Limited noise queries via Molang expressions |
| **Terrain Generation** | Can directly modify terrain algorithms | Feature placement only, cannot rewrite terrain generation |
| **File Structure** | `data/<namespace>/worldgen/` with density_function, noise, placed_feature | `behavior_packs/` with features and biomes |
| **Flexibility** | Very high - modify any aspect of terrain | Limited - work within existing terrain system |

### Achieving Similar Effects in Bedrock Edition

To create terrain-aware features like boulders in Bedrock Edition:

**1. Use Feature Placement with Noise Queries**

Bedrock Edition supports noise-based queries in Molang expressions. Example for a custom feature:

```json
{
  "format_version": "1.13.0",
  "minecraft:scatter_feature": {
    "description": {
      "identifier": "mypack:boulder_feature"
    },
    "places_feature": "mypack:boulder_structure",
    "scatter_chance": {
      "numerator": 1,
      "denominator": 4
    },
    "x": {
      "distribution": "uniform",
      "extent": [0, 15]
    },
    "z": "q.noise(v.worldx, v.worldz) > 0.3 ? math.random(0, 15) : -1",
    "y": "q.heightmap(v.worldx, v.worldz)"
  }
}
```

**Key Bedrock Noise Queries:**
- `q.noise(x, z)` - Returns 2D Perlin noise value (-1.0 to 1.0)
- `q.heightmap(x, z)` - Returns terrain height at coordinates

**2. Limitations**

- Cannot access the full terrain noise system like Java Edition
- Cannot modify terrain shape itself, only place features on existing terrain
- Noise queries are simpler (2D only, limited parameters)
- Cannot reference vanilla noise patterns like "continentalness" or "erosion"

**3. Alternative Approaches**

For Bedrock Edition terrain-aware features:

- **Biome-based placement**: Define custom biomes that generate in specific terrain types
- **Height-based conditions**: Use `q.heightmap()` to place features based on elevation
- **Combined conditions**: Use Molang expressions combining noise, height, and biome checks

**Example - Height and Noise Based Boulder Placement:**

```json
{
  "format_version": "1.13.0",
  "minecraft:scatter_feature": {
    "description": {
      "identifier": "mypack:mountain_boulder"
    },
    "places_feature": "mypack:boulder",
    "scatter_chance": {
      "numerator": 1,
      "denominator": "q.heightmap(v.worldx, v.worldz) > 80 && q.noise(v.worldx * 0.1, v.worldz * 0.1) > 0.2 ? 2 : 10"
    }
  }
}
```

This places boulders with 1/2 (50%) chance in mountainous areas (height > 80 with high noise) and 1/10 (10%) chance elsewhere.

### Resources for Bedrock Edition

- **[Bedrock Wiki - Heightmap Noise](https://wiki.bedrock.dev/world-generation/heightmap-noise)**: Official guide for noise queries
- **[Microsoft Learn - World Generation](https://learn.microsoft.com/en-us/minecraft/creator/documents/world-generation)**: Bedrock world generation overview
- **[Bedrock Biome Generator](https://bedrockbiomegenerator.icedfoxstudios.com/)**: Tool for creating custom biomes

### Summary

For the **same effect as this guide** (terrain-aware boulder generation):
- **Java Edition**: Use this guide's approach with placed features and `noise_threshold_count`
- **Bedrock Edition**: Use scatter features with Molang noise queries like `q.noise()` and height checks

Bedrock Edition offers basic terrain-aware placement but cannot match Java Edition's deep integration with the noise-based terrain generation system.

---

## Extension Approaches

There are two main approaches to extending terrain generation with noise patterns:

1. **Using Noise in Placed Features**: Add custom decorations/features that respond to terrain characteristics
2. **Custom Density Functions**: Modify how terrain itself is generated by adding to the noise router

Choose based on your goal:
- **Use Placed Features** if you want to add things *on* or *in* existing terrain (trees, ores, boulders, structures)
- **Use Custom Density Functions** if you want to change the terrain shape itself (add floating islands, caves, overhangs)

## Approach 1: Using Noise in Placed Features

This approach lets you place features that respond to the existing terrain's characteristics without modifying the terrain generation itself.

### File Structure

Create files in your datapack under:
```
data/<namespace>/worldgen/
├── configured_feature/
│   └── my_feature.json
└── placed_feature/
    └── my_placed_feature.json
```

### Step 1: Create a Configured Feature

Define what you want to place. Example for a boulder:

**`data/boulders/worldgen/configured_feature/stone_boulder.json`**:
```json
{
  "type": "minecraft:random_patch",
  "config": {
    "tries": 3,
    "xz_spread": 5,
    "y_spread": 2,
    "feature": {
      "feature": {
        "type": "minecraft:simple_block",
        "config": {
          "to_place": {
            "type": "minecraft:simple_state_provider",
            "state": {
              "Name": "minecraft:stone"
            }
          }
        }
      },
      "placement": []
    }
  }
}
```

### Step 2: Create a Placed Feature with Noise-Based Placement

This is where you make your feature terrain-aware:

**`data/boulders/worldgen/placed_feature/terrain_aware_boulder.json`**:
```json
{
  "feature": "boulders:stone_boulder",
  "placement": [
    {
      "type": "minecraft:noise_threshold_count",
      "noise": "minecraft:ridge",
      "scale": 1.0,
      "above_threshold": 0.0,
      "below_threshold": 0
    },
    {
      "type": "minecraft:in_square"
    },
    {
      "type": "minecraft:heightmap",
      "heightmap": "WORLD_SURFACE_WG"
    },
    {
      "type": "minecraft:biome"
    }
  ]
}
```

**Key Placement Modifiers:**

- **`noise_threshold_count`**: Controls feature density based on a noise value
  - `noise`: Reference to a noise pattern (can be vanilla like "minecraft:ridge" or custom)
  - `scale`: How to scale the noise value
  - `above_threshold`: Minimum noise value to place the feature
  - `below_threshold`: How many features to place when below threshold

- **`heightmap`**: Places feature at surface level
  - `WORLD_SURFACE_WG`: Top solid block
  - `OCEAN_FLOOR_WG`: Ocean floor
  - `MOTION_BLOCKING`: Top motion-blocking block

- **`biome`**: Only places in valid biomes (defined elsewhere)

### Step 3: Add to Biomes

Reference your placed feature in biome files to make it spawn:

**`data/boulders/worldgen/biome/my_biome.json`** (partial):
```json
{
  "features": [
    [],
    [],
    [],
    [],
    [],
    [],
    ["boulders:terrain_aware_boulder"],
    [],
    [],
    []
  ]
}
```

The array index corresponds to decoration steps (see Minecraft wiki for the full list).

## Approach 2: Custom Density Functions

This approach modifies the terrain generation itself by adding custom density functions to the noise router.

### File Structure

```
data/<namespace>/worldgen/
├── density_function/
│   └── my_custom_function.json
├── noise/
│   └── my_custom_noise.json
└── noise_settings/
    └── my_settings.json
```

### Step 1: Define Custom Noise (Optional)

If you need a new noise pattern beyond vanilla ones:

**`data/boulders/worldgen/noise/boulder_noise.json`**:
```json
{
  "firstOctave": -7,
  "amplitudes": [1.0, 1.0, 0.5, 0.25],
  "type": "minecraft:normal"
}
```

**Parameters:**
- `firstOctave`: Starting octave (negative = larger features)
- `amplitudes`: Array controlling noise layers (more = more detail)
- `type`: "minecraft:normal" for standard Perlin-style noise

### Step 2: Create a Custom Density Function

Build logic that references the terrain's noise:

**`data/boulders/worldgen/density_function/boulder_density.json`**:
```json
{
  "type": "minecraft:mul",
  "argument1": {
    "type": "minecraft:noise",
    "noise": "boulders:boulder_noise",
    "xz_scale": 0.5,
    "y_scale": 1.0
  },
  "argument2": {
    "type": "minecraft:y_clamped_gradient",
    "from_y": 60,
    "to_y": 120,
    "from_value": 0.0,
    "to_value": 1.0
  }
}
```

**Common Density Function Types:**

- **`minecraft:noise`**: Samples a noise pattern
  - `noise`: Which noise to sample
  - `xz_scale`: Horizontal scale (lower = larger features)
  - `y_scale`: Vertical scale

- **`minecraft:add`**, **`minecraft:mul`**: Math operations on two functions
- **`minecraft:y_clamped_gradient`**: Value changes with Y level
- **`minecraft:clamp`**: Constrains output between min/max
- **`minecraft:min`**, **`minecraft:max`**: Picks minimum or maximum value

### Step 3: Reference Existing Terrain Density

To make your feature respond to existing terrain, reference vanilla density functions:

**`data/boulders/worldgen/density_function/terrain_scaled_boulder.json`**:
```json
{
  "type": "minecraft:mul",
  "argument1": "minecraft:overworld/base_3d_noise",
  "argument2": {
    "type": "minecraft:noise",
    "noise": "boulders:boulder_noise",
    "xz_scale": 0.25,
    "y_scale": 0.5
  }
}
```

This multiplies your custom noise by the vanilla terrain noise, making your feature stronger where terrain is more varied.

### Step 4: Integrate into Noise Settings

Add your density function to a dimension's noise settings:

**`data/boulders/worldgen/noise_settings/custom_settings.json`** (partial):
```json
{
  "noise_router": {
    "final_density": {
      "type": "minecraft:add",
      "argument1": "minecraft:overworld/caves/noodle",
      "argument2": "boulders:terrain_scaled_boulder"
    }
  },
  "surface_rule": { ... },
  "sea_level": 63,
  "ore_veins_enabled": true
}
```

**Note:** Modifying `final_density` affects whether blocks are solid or air. Be careful with values to avoid breaking terrain generation.

## Practical Example: Terrain-Aware Boulders

Let's create boulders that are large in mountainous terrain and small/rare in flat areas.

### Strategy

We'll use **Approach 1 (Placed Features)** with noise-based placement that responds to terrain variation.

### Implementation

**1. Create a boulder feature** - `configured_feature/boulder.json`:
```json
{
  "type": "minecraft:block_pile",
  "config": {
    "state_provider": {
      "type": "minecraft:weighted_state_provider",
      "entries": [
        {
          "weight": 3,
          "data": {
            "Name": "minecraft:stone"
          }
        },
        {
          "weight": 1,
          "data": {
            "Name": "minecraft:cobblestone"
          }
        }
      ]
    }
  }
}
```

**2. Create terrain-aware placement** - `placed_feature/mountain_boulder.json`:
```json
{
  "feature": "boulders:boulder",
  "placement": [
    {
      "type": "minecraft:noise_threshold_count",
      "noise": "minecraft:continentalness",
      "scale": 2.0,
      "above_threshold": 0.3,
      "below_threshold": 1
    },
    {
      "type": "minecraft:count",
      "count": {
        "type": "minecraft:weighted_list",
        "distribution": [
          {"weight": 1, "data": 1},
          {"weight": 3, "data": 2},
          {"weight": 2, "data": 3}
        ]
      }
    },
    {
      "type": "minecraft:in_square"
    },
    {
      "type": "minecraft:heightmap",
      "heightmap": "MOTION_BLOCKING"
    },
    {
      "type": "minecraft:biome"
    }
  ]
}
```

**What this does:**
- Uses `continentalness` noise (which corresponds to terrain height variation)
- Places more boulders where noise is above 0.3 (mountainous areas)
- Places 1-3 boulders per attempt using weighted distribution
- Places at surface level

### Testing

1. Create your datapack structure
2. Add files to `datapacks/` folder in your world save
3. Run `/reload` in-game
4. Create a new world or explore new chunks

## Best Practices

### 1. Start with Vanilla References

Reference existing vanilla density functions and noise patterns rather than creating everything from scratch:

```json
{
  "type": "minecraft:add",
  "argument1": "minecraft:overworld/base_3d_noise",
  "argument2": { ... your custom addition ... }
}
```

### 2. Scale Carefully

- Lower `xz_scale` = larger, smoother features
- Higher `xz_scale` = smaller, more chaotic features
- Start with vanilla values and adjust incrementally

### 3. Test Incrementally

- Add one feature at a time
- Test in superflat or single-biome worlds first
- Use `/locate` and creative mode flying to verify placement

### 4. Use Appropriate Noise Types

Different noise patterns serve different purposes:
- `minecraft:ridge`: Good for ridges and cliffs
- `minecraft:continentalness`: Terrain height/landmass
- `minecraft:erosion`: Terrain smoothness
- `minecraft:temperature`: Climate-based features

### 5. Consider Performance

- Complex density functions run for every block
- Use `minecraft:cache_once` or `minecraft:cache_all_in_cell` for expensive operations
- Limit the number of placed features per chunk

### 6. Document Your Namespace

Use clear, descriptive names:
- `boulders:mountain_boulder_large` ✓
- `boulders:thing1` ✗

## Troubleshooting

### Features Not Appearing

**Check:**
1. Files are in correct directory structure
2. JSON syntax is valid (use a validator)
3. Feature is added to biome generation steps
4. Biome exists and you're in the right place
5. Run `/reload` after changes

### Features Too Dense/Sparse

**Adjust:**
- `noise_threshold_count` parameters
- `count` modifier values
- Chunk generation frequency in biome files

### Wrong Terrain Response

**Verify:**
- You're using the right noise reference
- `scale` parameter is appropriate
- `above_threshold` value makes sense (typical range: -1.0 to 1.0)

### JSON Syntax Errors

**Common issues:**
- Missing commas between array elements
- Trailing commas at end of objects/arrays
- Unmatched brackets or braces
- Incorrect string quotes (must be double quotes `"`)

**Solution:** Use an online JSON validator or IDE with JSON support.

### Changes Not Applying

- Run `/reload` command in-game
- Existing chunks won't regenerate - explore new areas
- Check game logs for datapack errors
- Ensure datapack is enabled: `/datapack list`

## Useful Tools

### Generators and Validators

- **[Misode's Data Pack Generators](https://misode.github.io/)**: Generate worldgen JSON files with validation
- **[Jacobsjo's Minecraft Worldgen Simulator](https://jacobsjo.eu/mc/)**: Visualize worldgen changes
- **[JSON Lint](https://jsonlint.com/)**: Validate JSON syntax

### Documentation

- **[Minecraft Wiki - Custom World Generation](https://minecraft.wiki/w/Custom_world_generation)**
- **[Minecraft Wiki - Placed Feature](https://minecraft.wiki/w/Placed_feature)**
- **[Minecraft Wiki - Density Function](https://minecraft.wiki/w/Density_function)**

### Community Resources

- **r/MinecraftCommands** subreddit
- **Minecraft Commands Discord server**
- **Planet Minecraft** tutorials and examples

## Next Steps

Now that you understand how to extend noise patterns:

1. Experiment with different noise types
2. Combine multiple density functions
3. Create complex placement conditions
4. Study vanilla worldgen files in your Minecraft installation
5. Share your creations with the community!

Remember: worldgen is complex and requires experimentation. Don't be afraid to iterate and test different approaches.
