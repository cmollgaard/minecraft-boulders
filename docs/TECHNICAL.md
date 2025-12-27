# Technical Documentation

This document provides technical details about the Minecraft Boulders datapack implementation, including information about Minecraft's noise patterns and how to extend them for custom features.

## Table of Contents

1. [Datapack Structure](#datapack-structure)
2. [Understanding Noise Patterns](#understanding-noise-patterns)
3. [Density Functions](#density-functions)
4. [Extending Terrain Generation](#extending-terrain-generation)
5. [Visualization Tools](#visualization-tools)
6. [Version Compatibility](#version-compatibility)
7. [Bedrock Edition Differences](#bedrock-edition-differences)

---

## Datapack Structure

```
minecraft-boulders/
├── pack.mcmeta                               # Datapack metadata (format 18)
├── LICENSE                                   # MIT License
├── docs/                                     # Documentation
│   ├── README.md                            # Main documentation
│   ├── CONFIGURATION.md                     # Configuration guide
│   ├── TECHNICAL.md                         # This file
│   └── CONTRIBUTING.md                      # Contributing guidelines
├── experiments/                             # Noise visualization tools
│   ├── visualize_noise.py
│   └── README.md
└── data/
    └── boulders/
        └── worldgen/
            ├── configured_feature/           # Boulder block patterns
            │   ├── small_boulder.json       # 2-5 blocks (tries: 3, xz_spread: 2)
            │   ├── medium_boulder.json      # 6-12 blocks (tries: 6, xz_spread: 3)
            │   └── large_boulder.json       # 13-25 blocks (tries: 12, xz_spread: 4)
            ├── placed_feature/               # Placement rules
            │   ├── small_boulder.json       # Y=50-160, rarity: 12
            │   ├── medium_boulder.json      # Y=70-180, rarity: 8
            │   └── large_boulder.json       # Y=90-200, rarity: 5
            └── density_function/             # Terrain-aware distribution
                ├── terrain_height_factor.json
                └── boulder_density.json
```

---

## Understanding Noise Patterns

Minecraft's terrain generation in versions 1.18+ uses a sophisticated noise-based system to create natural-looking terrain, caves, biomes, and other world features.

### What is Noise?

In procedural generation, "noise" refers to mathematical functions that produce pseudo-random, continuous values. Unlike pure randomness, noise functions create smooth, natural-looking patterns.

**Why Use Noise?**
- **Natural Appearance**: Creates organic-looking terrain
- **Reproducibility**: Same seed produces the same world
- **Scalability**: Works at any scale
- **Customizability**: Parameters can create vastly different terrain

### Noise Types

Minecraft primarily uses two types of gradient noise:

**Perlin Noise**
- Creates smooth, rolling terrain features
- Good for continental shapes and large-scale features

**Simplex Noise**
- Less directional bias than Perlin noise
- Faster to compute in higher dimensions

**3D Noise**
- Used specifically for cave generation
- Creates interconnected cave networks

### Noise Parameters

| Parameter | Description | Effect |
|-----------|-------------|--------|
| Octaves | Number of noise layers | More = more detail |
| Amplitudes | Strength of each octave | Higher = more pronounced |
| Frequency | How "tight" the pattern | Higher = more features |
| Seed | Random number generator seed | Different = different world |

### Practical Example: Boulder Placement

To place boulders naturally using noise:

1. Generate a 2D noise value at each X, Z coordinate
2. If noise value > threshold: "Place a boulder here"
3. Result: Boulders appear in clusters (where noise is high) but not everywhere

**What You Control:**
- **Threshold**: Higher values = fewer, rarer boulders
- **Frequency**: Large scale = boulder fields, small scale = scattered boulders
- **Octaves**: More = boulder patterns have variation within patterns

---

## Density Functions

Density functions are the mathematical building blocks that determine whether a specific coordinate should be air, solid block, or fluid.

### Basic Types

#### Constant
```json
{
  "type": "constant",
  "value": 0.5
}
```

#### Noise
```json
{
  "type": "noise",
  "noise": "minecraft:terrain",
  "xz_scale": 1.0,
  "y_scale": 1.0
}
```

### Mathematical Operations

#### Add
```json
{
  "type": "add",
  "argument1": { "type": "constant", "value": 1.0 },
  "argument2": { "type": "noise", "noise": "minecraft:terrain" }
}
```

#### Multiply (mul)
```json
{
  "type": "mul",
  "argument1": { "type": "constant", "value": 0.5 },
  "argument2": { "type": "noise", "noise": "minecraft:ridges" }
}
```

#### Min/Max
```json
{
  "type": "min",
  "argument1": { "type": "noise", "noise": "minecraft:terrain" },
  "argument2": { "type": "constant", "value": 0.8 }
}
```

### Transformation Functions

#### Y Clamped Gradient
Gradually changes values across the vertical axis:
```json
{
  "type": "y_clamped_gradient",
  "from_y": -64,
  "to_y": 320,
  "from_value": 1.0,
  "to_value": -1.0
}
```

#### Clamp
Restricts output to a specific range:
```json
{
  "type": "clamp",
  "input": { "type": "noise", "noise": "minecraft:terrain" },
  "min": -1.0,
  "max": 1.0
}
```

### This Datapack's Density Functions

**terrain_height_factor.json**
- Maps terrain height (Y=60-200) to boulder probability
- Uses `y_clamped_gradient` combined with offset noise

**boulder_density.json**
- Combines height factor with calcite noise
- Creates natural, clustered boulder distribution

---

## Extending Terrain Generation

There are two main approaches to extending terrain generation:

### Approach 1: Using Noise in Placed Features

Add custom decorations/features that respond to terrain characteristics.

**File Structure:**
```
data/<namespace>/worldgen/
├── configured_feature/
│   └── my_feature.json
└── placed_feature/
    └── my_placed_feature.json
```

**Key Placement Modifiers:**

- `noise_threshold_count`: Controls feature density based on noise value
- `heightmap`: Places feature at surface level
- `biome`: Only places in valid biomes
- `rarity_filter`: Controls spawn frequency
- `environment_scan`: Finds solid ground for placement

### Approach 2: Custom Density Functions

Modify how terrain itself is generated.

**Creating Custom Noise:**
```json
{
  "firstOctave": -7,
  "amplitudes": [1.0, 1.0, 0.5, 0.25],
  "type": "minecraft:normal"
}
```

**Custom Density Function:**
```json
{
  "type": "minecraft:mul",
  "argument1": {
    "type": "minecraft:noise",
    "noise": "custom:my_noise",
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

### Best Practices

1. **Start with Vanilla References**: Reference existing vanilla density functions
2. **Scale Carefully**: Lower `xz_scale` = larger features
3. **Test Incrementally**: Add one feature at a time
4. **Use Appropriate Noise Types**: Different noises serve different purposes
5. **Consider Performance**: Complex density functions run for every block

---

## Visualization Tools

The `experiments/` folder contains Python scripts to visualize Minecraft-style noise patterns.

### Setup

```bash
cd experiments
pip install -r requirements.txt
```

### Usage

```bash
# Basic visualization
python visualize_noise.py

# With custom seed
python visualize_noise.py --seed 42

# Interactive display with 3D visualization
python visualize_noise.py --show

# Custom output
python visualize_noise.py --seed 67890 --size 200 --output terrain_67890.png
```

### Output

The visualization shows:
1. **Continentalness** - Base terrain
2. **Erosion** - Terrain smoothness variation
3. **Ridges** - Mountain ridge patterns
4. **Boulder Noise** - Example custom feature noise
5. **Combined** - Base terrain with boulder noise overlay

See `experiments/README.md` for detailed documentation.

---

## Version Compatibility

This datapack targets:

- **Primary**: Minecraft Java Edition 1.20+ (pack_format 18)
- **Declared Support**: pack_format 15-18

### Version Notes

- **1.18.x**: Introduction of the new noise system
- **1.19.x**: Refinements and optimizations
- **1.20.x**: Additional features and density functions
- **1.21.x**: Latest improvements and stability

The core worldgen concepts remain consistent across these versions.

---

## Bedrock Edition Differences

> ⚠️ **This datapack is Java Edition only.** Bedrock Edition uses a completely different system.

### Key Differences

| Feature | Java Edition | Bedrock Edition |
|---------|--------------|-----------------|
| **Customization** | Datapacks with JSON worldgen | Add-ons with JSON + scripts |
| **Noise Access** | Full control over density functions | Limited via Molang expressions |
| **Terrain Generation** | Can directly modify algorithms | Feature placement only |
| **File Structure** | `data/<namespace>/worldgen/` | `behavior_packs/` |
| **Flexibility** | Very high | Limited |

### Achieving Similar Effects in Bedrock

For Bedrock Edition, use scatter features with Molang noise queries:

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
      "denominator": "q.heightmap(v.worldx, v.worldz) > 80 && q.noise(v.worldx * 0.1, v.worldz * 0.1) > 0.2 ? 2 : 10"
    }
  }
}
```

**Key Bedrock Noise Queries:**
- `q.noise(x, z)` - Returns 2D Perlin noise value (-1.0 to 1.0)
- `q.heightmap(x, z)` - Returns terrain height at coordinates

### Bedrock Resources

- [Bedrock Wiki - Heightmap Noise](https://wiki.bedrock.dev/world-generation/heightmap-noise)
- [Microsoft Learn - World Generation](https://learn.microsoft.com/en-us/minecraft/creator/documents/world-generation)
- [Bedrock Biome Generator](https://bedrockbiomegenerator.icedfoxstudios.com/)

---

## External Resources

### Official Documentation

- [Minecraft Wiki - Noise Settings](https://minecraft.wiki/w/Noise_settings)
- [Minecraft Wiki - Noise Router](https://minecraft.wiki/w/Noise_router)
- [Minecraft Wiki - Density Functions](https://minecraft.wiki/w/Density_function)
- [Minecraft Wiki - Noise](https://minecraft.wiki/w/Noise)

### Online Tools

- [Misode's Data Pack Generators](https://misode.github.io/) - Visual editor for worldgen
- [Jacobsjo's Worldgen Simulator](https://jacobsjo.eu/mc/) - Visualize worldgen changes
- [JSON Lint](https://jsonlint.com/) - Validate JSON syntax

### Community Resources

- [Misode's Guides](https://misode.github.io/guides/) - Comprehensive data pack guides
- [Fruitful Generator Guides](https://fruitful-generator.github.io/guides/density-functions/) - Detailed density function explanations
- r/MinecraftCommands subreddit
- Minecraft Commands Discord server
