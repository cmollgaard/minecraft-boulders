# Minecraft Noise Patterns: A Comprehensive Guide

## Overview

Minecraft's terrain generation in versions 1.18 and later (including 1.20 and 1.21) uses a sophisticated noise-based system to create natural-looking terrain, caves, biomes, and other world features. This document explains how these noise patterns work and how they can be customized through datapacks.

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Noise Types](#noise-types)
3. [Noise Parameters](#noise-parameters)
4. [Noise Router](#noise-router)
5. [Density Functions](#density-functions)
6. [Multi-Noise Biome System](#multi-noise-biome-system)
7. [Practical Examples](#practical-examples)
8. [Resources and Tools](#resources-and-tools)

---

## Core Concepts

### What is Noise?

In the context of procedural generation, "noise" refers to mathematical functions that produce pseudo-random, continuous values. Unlike pure randomness, noise functions create smooth, natural-looking patterns that can simulate real-world features like terrain elevation, cloud formations, or mineral distributions.

### Why Use Noise for Terrain Generation?

- **Natural Appearance**: Noise creates organic-looking terrain rather than jagged, artificial patterns
- **Reproducibility**: Using a seed value ensures the same world can be regenerated consistently
- **Scalability**: Noise functions work at any scale, from small details to continental features
- **Customizability**: Parameters can be adjusted to create vastly different terrain styles

---

## Noise Types

Minecraft primarily uses two types of gradient noise:

### Perlin Noise

- **Purpose**: Creates smooth, rolling terrain features
- **Implementation**: Minecraft uses "improved" Perlin noise, which averages two 3D Perlin samples
- **Characteristics**: 
  - Smooth gradients between hills and valleys
  - Natural-looking elevation changes
  - Good for continental shapes and large-scale features

### Simplex Noise

- **Purpose**: Generates varied terrain features with better computational efficiency
- **Characteristics**:
  - Less directional bias than Perlin noise
  - Faster to compute, especially in higher dimensions
  - Used for specific biome features and terrain variations

### 3D Noise

- **Purpose**: Used specifically for cave generation
- **How it Works**: Unlike 2D noise (which varies across X and Z coordinates), 3D noise also considers the Y (vertical) axis
- **Result**: Creates intricate, interconnected cave networks with multiple levels, rather than simple horizontal tunnels

---

## Noise Parameters

Noise functions are configured using several key parameters:

### Octaves

**Definition**: The number of noise layers stacked together, each at a different frequency and amplitude.

- **More Octaves**: Creates more detailed, rugged terrain with fine features
- **Fewer Octaves**: Produces smoother, simpler terrain
- **Example**: With 4 octaves, you get large hills (octave 1) + medium details (octave 2) + small bumps (octave 3) + tiny variations (octave 4)

### Amplitudes

**Definition**: An array of values controlling the strength/influence of each octave.

- **Higher Amplitude**: That octave's features are more pronounced
- **Lower Amplitude**: That octave's features are subtler
- **Pattern**: Typically decreases for higher octaves (e.g., `[1.0, 0.5, 0.25, 0.125]`)

### Frequency

**Definition**: How "tight" or "busy" the noise pattern is.

- **High Frequency**: Dense, busy terrain with many small features close together
- **Low Frequency**: Spacious, smooth terrain with features spread far apart
- **Calculation**: For octave at index n: `2^(-firstOctave + n)`

### First Octave

**Definition**: The starting octave index, affecting the base frequency of the noise.

- **Negative Values**: Start with larger, smoother features
- **Positive Values**: Start with smaller, tighter patterns

### Seed

**Definition**: The initial value for the random number generator.

- **Same Seed**: Always produces the same world
- **Different Seeds**: Creates completely different worlds
- **Usage**: Allows world sharing and reproducibility

### JSON Format Example

```json
{
  "firstOctave": -2,
  "amplitudes": [1.0, 0.5, 0.25, 0.125]
}
```

---

## Noise Router

The noise router is the central configuration system introduced in Minecraft 1.18+ that determines how various noise functions interact to produce the final terrain.

### Configuration Location

In datapacks: `data/<namespace>/worldgen/noise_settings/<custom_settings>.json`

### Noise Router Structure

The noise router contains references to density functions that control different aspects of world generation:

```json
"noise_router": {
  "barrier": "minecraft:barrier",
  "fluid_level_floodedness": "minecraft:floodedness",
  "fluid_level_spread": "minecraft:fluid_spread",
  "lava": "minecraft:lava",
  "temperature": "minecraft:temperature",
  "vegetation": "minecraft:vegetation",
  "continents": "minecraft:continents",
  "erosion": "minecraft:erosion",
  "depth": "minecraft:depth",
  "ridges": "minecraft:ridges",
  "initial_density_without_jaggedness": "minecraft:initial_density",
  "final_density": "minecraft:final_density",
  "vein_toggle": "minecraft:vein_toggle",
  "vein_ridged": "minecraft:vein_ridged",
  "vein_gap": "minecraft:vein_gap"
}
```

### Key Noise Router Fields

#### Terrain Shape
- **continents**: Controls land vs water distribution (continentalness)
- **erosion**: Affects how worn-down or sharp terrain features appear
- **depth**: Influences overall terrain height
- **ridges**: Creates mountain ridges and peaks

#### Caves and Underground
- **barrier**: Separates aquifers from open caves
- **fluid_level_floodedness**: Controls liquid generation in caves
- **fluid_level_spread**: Determines horizontal fluid spread
- **lava**: Decides if aquifers contain lava or water

#### Biome Mapping
- **temperature**: Used for biome temperature determination
- **vegetation**: Affects vegetation density in biomes

#### Terrain Density
- **initial_density_without_jaggedness**: Base density for aquifer and surface rules
- **final_density**: Final terrain cutoff (positive = solid, negative = air)

#### Ore Generation
- **vein_toggle**: Enables/disables ore vein generation
- **vein_ridged**: Controls ore vein patterns
- **vein_gap**: Creates gaps in ore veins

---

## Density Functions

Density functions are the mathematical building blocks used in the noise router. They determine whether a specific coordinate should be air, solid block, or fluid.

### Basic Density Function Types

#### Constant
Returns the same value everywhere.

```json
{
  "type": "constant",
  "value": 0.5
}
```

**Use Case**: Flat terrain baseline, threshold values

#### Noise
Uses Perlin or Simplex noise to generate values.

```json
{
  "type": "noise",
  "noise": "minecraft:terrain",
  "xz_scale": 1.0,
  "y_scale": 1.0
}
```

**Use Case**: Terrain elevation, cave patterns, biome boundaries

### Mathematical Operations

#### Add
Combines two density functions by adding their values.

```json
{
  "type": "add",
  "argument1": { "type": "constant", "value": 1.0 },
  "argument2": { "type": "noise", "noise": "minecraft:terrain" }
}
```

**Use Case**: Layering terrain features, combining multiple noise patterns

#### Multiply (mul)
Multiplies two density function values.

```json
{
  "type": "mul",
  "argument1": { "type": "constant", "value": 0.5 },
  "argument2": { "type": "noise", "noise": "minecraft:ridges" }
}
```

**Use Case**: Scaling terrain intensity, damping effects

#### Min/Max
Selects the minimum or maximum of two values.

```json
{
  "type": "min",
  "argument1": { "type": "noise", "noise": "minecraft:terrain" },
  "argument2": { "type": "constant", "value": 0.8 }
}
```

**Use Case**: Terrain limits, cave floor/ceiling definition

### Transformation Functions

#### Abs, Square, Cube
Transform input mathematically.

```json
{
  "type": "abs",
  "argument": { "type": "noise", "noise": "minecraft:caves" }
}
```

**Use Case**: Shaping terrain gradients, creating symmetrical features

#### Clamp
Restricts output to a specific range.

```json
{
  "type": "clamp",
  "input": { "type": "noise", "noise": "minecraft:terrain" },
  "min": -1.0,
  "max": 1.0
}
```

**Use Case**: Preventing extreme terrain values, controlling generation bounds

### Advanced Functions

#### Spline
Uses a curve with control points for smooth interpolation.

```json
{
  "type": "spline",
  "spline": {
    "coordinate": { "type": "noise", "noise": "minecraft:continents" },
    "points": [
      {"location": -1.0, "value": -0.5, "derivative": 0.0},
      {"location": 0.0, "value": 0.0, "derivative": 0.5},
      {"location": 1.0, "value": 1.0, "derivative": 0.0}
    ]
  }
}
```

**Use Case**: Smooth transitions, rolling hills, dramatic cliffs

#### Y Clamped Gradient
Gradually changes values across the vertical axis.

```json
{
  "type": "y_clamped_gradient",
  "from_y": -64,
  "to_y": 320,
  "from_value": 1.0,
  "to_value": -1.0
}
```

**Use Case**: Voxel-based height variation, underground vs surface transitions

### Optimization Functions

#### Interpolated
Smooths input across a cell for efficient sampling.

```json
{
  "type": "interpolated",
  "argument": { "type": "noise", "noise": "minecraft:terrain" }
}
```

#### Flat Cache
Computes values per 4x4 column, caching for performance.

```json
{
  "type": "flat_cache",
  "argument": { "type": "noise", "noise": "minecraft:continents" }
}
```

#### Cache 2D
Computes once per horizontal position.

```json
{
  "type": "cache_2d",
  "argument": { "type": "noise", "noise": "minecraft:erosion" }
}
```

**Use Case**: Performance optimization for expensive calculations

### Blending Functions

#### Blend Alpha, Blend Offset, Blend Density
Handle smooth transitions between biomes and terrain types.

```json
{
  "type": "blend_alpha"
}
```

**Use Case**: Biome blending, smooth terrain transitions

---

## Multi-Noise Biome System

Since Minecraft 1.18, biomes are no longer placed based solely on temperature bands. Instead, they use a "multi-noise" system.

### How It Works

1. **Multiple Noise Fields**: Several independent noise functions generate values:
   - **Temperature**: Hot to cold
   - **Humidity**: Dry to wet
   - **Continentalness**: Ocean to inland
   - **Erosion**: Flat to mountainous
   - **Weirdness**: Normal to unusual terrain
   - **Depth**: Underground to surface

2. **Biome Mapping**: Each biome is assigned a "target range" for each parameter

3. **Point Selection**: For any world coordinate, all six noise values are calculated

4. **Best Match**: The biome whose target range best matches the calculated values is placed

### Benefits

- **Natural Transitions**: Biomes blend more organically
- **Complex Shapes**: Biomes aren't limited to simple bands or zones
- **Elevation Independence**: Temperature can vary at same elevation
- **Greater Variety**: More interesting biome distributions

### Example Biome Parameters

```json
{
  "biome": "minecraft:plains",
  "parameters": {
    "temperature": [0.0, 0.5],
    "humidity": [0.0, 0.5],
    "continentalness": [0.0, 0.3],
    "erosion": [-0.2, 0.2],
    "weirdness": [-0.3, 0.3],
    "depth": 0.0,
    "offset": 0.0
  }
}
```

---

## Practical Examples

### Example 1: Basic Noise Settings JSON

Complete noise settings configuration for a custom dimension:

```json
{
  "sea_level": 63,
  "disable_mob_generation": false,
  "ore_veins_enabled": true,
  "aquifers_enabled": true,
  "legacy_random_source": false,
  "default_block": {
    "Name": "minecraft:stone"
  },
  "default_fluid": {
    "Name": "minecraft:water",
    "Properties": {
      "level": "0"
    }
  },
  "noise": {
    "min_y": -64,
    "height": 384,
    "size_horizontal": 2,
    "size_vertical": 1
  },
  "noise_router": {
    "barrier": "minecraft:barrier",
    "fluid_level_floodedness": "minecraft:floodedness",
    "fluid_level_spread": "minecraft:fluid_spread",
    "lava": "minecraft:lava",
    "temperature": "minecraft:temperature",
    "vegetation": "minecraft:vegetation",
    "continents": "minecraft:continents",
    "erosion": "minecraft:erosion",
    "depth": "minecraft:depth",
    "ridges": "minecraft:ridges",
    "initial_density_without_jaggedness": "minecraft:initial_density",
    "final_density": "minecraft:final_density",
    "vein_toggle": "minecraft:vein_toggle",
    "vein_ridged": "minecraft:vein_ridged",
    "vein_gap": "minecraft:vein_gap"
  },
  "surface_rule": {
    "type": "minecraft:sequence",
    "sequence": []
  }
}
```

### Example 2: Custom Final Density Function

Creating custom terrain with combined noise:

```json
{
  "type": "add",
  "argument1": {
    "type": "noise",
    "noise": "minecraft:terrain",
    "xz_scale": 1.0,
    "y_scale": 1.0
  },
  "argument2": {
    "type": "mul",
    "argument1": {
      "type": "constant",
      "value": 0.5
    },
    "argument2": {
      "type": "noise",
      "noise": "minecraft:ridges",
      "xz_scale": 1.5,
      "y_scale": 1.0
    }
  }
}
```

**Result**: Base terrain with 50% strength ridge features added on top.

### Example 3: Creating Smooth Mountains

Using spline for gradual mountain formation:

```json
{
  "type": "spline",
  "spline": {
    "coordinate": {
      "type": "noise",
      "noise": "minecraft:continents"
    },
    "points": [
      {
        "location": -1.0,
        "value": -0.8,
        "derivative": 0.0
      },
      {
        "location": -0.5,
        "value": -0.2,
        "derivative": 0.2
      },
      {
        "location": 0.0,
        "value": 0.0,
        "derivative": 0.5
      },
      {
        "location": 0.5,
        "value": 0.5,
        "derivative": 1.0
      },
      {
        "location": 1.0,
        "value": 1.5,
        "derivative": 0.5
      }
    ]
  }
}
```

**Result**: Ocean floor (-1.0) → Coast (-0.5) → Plains (0.0) → Hills (0.5) → Mountains (1.0)

### Example 4: Cave Generation

Creating cheese caves using 3D noise:

```json
{
  "type": "noise",
  "noise": "minecraft:cheese_caves",
  "xz_scale": 1.0,
  "y_scale": 0.5
}
```

Combined with threshold check:

```json
{
  "type": "add",
  "argument1": {
    "type": "noise",
    "noise": "minecraft:cheese_caves",
    "xz_scale": 1.0,
    "y_scale": 0.5
  },
  "argument2": {
    "type": "mul",
    "argument1": {
      "type": "constant",
      "value": 0.2
    },
    "argument2": {
      "type": "y_clamped_gradient",
      "from_y": -64,
      "to_y": 320,
      "from_value": 1.0,
      "to_value": -1.0
    }
  }
}
```

**Result**: 3D cave network with density varying by height.

### Example 5: Defining Custom Noise

Creating a custom noise in `data/<namespace>/worldgen/noise/<name>.json`:

```json
{
  "firstOctave": -7,
  "amplitudes": [1.0, 1.0, 0.5, 0.25]
}
```

**Parameters**:
- Starts at octave -7 (very large features)
- 4 octaves with decreasing amplitudes
- Creates smooth, large-scale terrain variations

---

## Resources and Tools

### Official Documentation

- **Minecraft Wiki - Noise Settings**: [minecraft.wiki/w/Noise_settings](https://minecraft.wiki/w/Noise_settings)
- **Minecraft Wiki - Noise Router**: [minecraft.wiki/w/Noise_router](https://minecraft.wiki/w/Noise_router)
- **Minecraft Wiki - Density Functions**: [minecraft.wiki/w/Density_function](https://minecraft.wiki/w/Density_function)
- **Minecraft Wiki - Noise**: [minecraft.wiki/w/Noise](https://minecraft.wiki/w/Noise)

### Online Generators and Tools

- **Misode's Noise Settings Generator**: [misode.github.io/worldgen/noise-settings/](https://misode.github.io/worldgen/noise-settings/)
  - Visual editor for noise settings
  - Exports valid JSON for datapacks
  - Supports Minecraft 1.18 through 1.21+

- **Syldium Worldgen Generator**: [worldgen.syldium.dev/worldgen/noise_settings/](https://worldgen.syldium.dev/worldgen/noise_settings/)
  - Alternative noise settings generator
  - User-friendly interface
  - Supports multiple Minecraft versions

- **Misode's Data Pack Guides**: [misode.github.io/guides/](https://misode.github.io/guides/)
  - Comprehensive guides on data pack creation
  - Interactive examples and documentation

### Development Libraries

- **mc_noise_java**: [github.com/SeedFinding/mc_noise_java](https://github.com/SeedFinding/mc_noise_java)
  - Java library for simulating Minecraft noise
  - Implements Perlin and Simplex noise
  - Useful for external tools and analysis

### Plugins and Mods

- **WorldEdit with NoisyPatterns**: [modrinth.com/plugin/noisypatterns](https://modrinth.com/plugin/noisypatterns)
  - Allows using noise patterns for WorldEdit selections
  - Create custom terrain in-game
  - Experiment with noise parameters

- **More Density Functions**: [curseforge.com/minecraft/mc-mods/more-density-functions](https://www.curseforge.com/minecraft/mc-mods/more-density-functions)
  - Adds additional density function types
  - Worley/Voronoi noise support
  - Enhanced terrain customization

### Community Resources

- **Fruitful Generator Guides**: [fruitful-generator.github.io/guides/density-functions/](https://fruitful-generator.github.io/guides/density-functions/)
  - Detailed density function explanations
  - Practical examples and use cases

- **GitHub Gists and Examples**:
  - Misode's density function examples
  - Community-shared configurations
  - Real-world datapack examples

---

## Tips for Working with Noise Patterns

### Performance Considerations

1. **Use Caching Functions**: `flat_cache`, `cache_2d`, and `cache_once` reduce redundant calculations
2. **Limit Octaves**: More octaves = more detail but slower generation
3. **Optimize Density Functions**: Simpler functions generate faster
4. **Test Incrementally**: Generate small areas first to verify performance

### Design Best Practices

1. **Start Simple**: Begin with basic noise and add complexity gradually
2. **Use Splines for Smooth Transitions**: Better than stepped functions
3. **Balance Amplitudes**: Keep realistic proportions between octaves
4. **Test at Different Scales**: Verify terrain looks good both close-up and from distance
5. **Combine Multiple Noises**: Layer different patterns for natural variation

### Common Pitfalls

1. **Extreme Values**: Can create impossible terrain or void areas
2. **Unbalanced Octaves**: Too much detail or too smooth
3. **Missing Cache Functions**: Poor performance with complex calculations
4. **Ignoring Y-Axis**: 2D noise for caves creates unnatural flat layers
5. **Too Many Dependencies**: Complex router configurations are hard to debug

### Debugging Techniques

1. **Visualize Individual Functions**: Test each density function separately
2. **Use Constants**: Replace complex functions with constants to isolate issues
3. **Check Value Ranges**: Ensure density functions output expected ranges
4. **Test in Superflat**: Easier to see generation patterns
5. **Use /locate and /fill**: Quickly test specific coordinates

---

## Conclusion

Minecraft's noise-based world generation is a powerful and flexible system that allows for endless terrain variety. By understanding noise types, parameters, the noise router, and density functions, you can create custom worlds ranging from subtle variations of vanilla terrain to completely unique dimensions.

The key to mastering Minecraft noise patterns is experimentation. Use the tools and resources provided, start with simple modifications, and gradually build up complexity as you become comfortable with how different parameters affect the final result.

Whether you're creating a datapack for boulder placement, custom biomes, unique cave systems, or entirely new dimensions, understanding these fundamental concepts will enable you to harness the full power of Minecraft's world generation system.

---

## Version Compatibility

This guide covers Minecraft Java Edition versions:
- **1.18.x**: Introduction of the new noise system
- **1.19.x**: Refinements and optimizations
- **1.20.x**: Additional features and density functions
- **1.21.x**: Latest improvements and stability

The core concepts remain consistent across these versions, though specific parameters and available functions may vary slightly. Always refer to the official Minecraft Wiki for version-specific details.

---

*Last Updated: December 2025*
*For the minecraft-boulders project by cmollgaard*
