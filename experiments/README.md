# Noise Pattern Visualization Experiments

This folder contains tools for visualizing Minecraft-style noise patterns to help understand how they affect terrain generation.

## Purpose

When extending Minecraft's terrain generation with custom noise patterns (like adding boulders), it's helpful to visualize:
- How the base terrain noise looks
- How your custom noise pattern appears
- How they combine together
- The effect of different seeds and parameters

## Setup

### Requirements

- Python 3.8 or higher
- pip (Python package manager)

### Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install numpy matplotlib noise
```

## Usage

### Basic Usage

Generate a visualization with default settings:

```bash
python visualize_noise.py
```

This creates `noise_comparison.png` showing:
1. **Continentalness** - Base terrain (simulates Minecraft's continentalness noise)
2. **Erosion** - Terrain smoothness variation
3. **Ridges** - Mountain ridge patterns
4. **Boulder Noise** - Example custom feature noise
5. **Combined** - Base terrain with boulder noise overlay

### Custom Seed

Try different seeds to see how terrain varies:

```bash
python visualize_noise.py --seed 42
python visualize_noise.py --seed 99999
python visualize_noise.py --seed 2024
```

### Interactive Display

Show plots interactively (including 3D visualization):

```bash
python visualize_noise.py --show
```

### Different Map Size

Generate larger or smaller noise maps:

```bash
python visualize_noise.py --size 256  # Larger, more detail
python visualize_noise.py --size 64   # Smaller, faster
```

### Custom Output File

Specify output filename:

```bash
python visualize_noise.py --output my_terrain_seed_12345.png
```

### Complete Example

```bash
python visualize_noise.py --seed 67890 --size 200 --output terrain_67890.png --show
```

## Understanding the Visualizations

### 2D Views (Top Row)

Heatmaps showing noise values from a top-down perspective:
- **Warm colors** (red/yellow): High values (mountains, feature placement likely)
- **Cool colors** (blue/green): Low values (valleys, feature placement unlikely)

### Contour Views (Bottom Row)

Contour lines show elevation levels, like a topographic map:
- **Dense contour lines**: Steep terrain changes
- **Sparse contour lines**: Flat or gradual slopes

### 3D Views (Interactive Mode)

When using `--show`, you'll see 3D surface plots showing:
- **Height**: Noise value magnitude
- **X/Z axes**: Horizontal coordinates (like Minecraft's X and Z)
- **Rotation**: Click and drag to rotate the view

## Noise Types Explained

### Continentalness
- **Scale**: Large (200.0)
- **Octaves**: 6
- **Purpose**: Defines major landmasses vs oceans
- **In Minecraft**: Controls whether terrain is inland or coastal

### Erosion
- **Scale**: Medium (80.0)
- **Octaves**: 5
- **Purpose**: Creates terrain variation and smoothness
- **In Minecraft**: Determines how rough or smooth terrain appears

### Ridges
- **Scale**: Medium (60.0)
- **Processing**: Uses absolute values to create peaks
- **Purpose**: Generates mountain ridges and sharp features
- **In Minecraft**: Used for dramatic mountain ranges

### Boulder Noise (Custom)
- **Scale**: Small (30.0)
- **Octaves**: 3
- **Purpose**: Example of a custom feature layer
- **Usage**: Could control boulder density/size in your datapack

## Modifying for Your Needs

### Create Custom Noise Patterns

Edit `visualize_noise.py` and add your own noise generator:

```python
def generate_my_custom_noise(self):
    """My custom noise for specific features."""
    return self.generate_perlin_noise(
        octaves=4,      # More octaves = more detail
        scale=100.0,    # Larger scale = smoother, bigger features
        persistence=0.5 # Controls amplitude decay
    )
```

Then add it to the comparison in `main()`:

```python
my_noise = visualizer.generate_my_custom_noise()
noise_maps.append(my_noise)
titles.append('My Custom Feature')
```

### Adjust Noise Parameters

Key parameters to experiment with:

- **octaves**: Number of detail layers (1-8)
  - More octaves = more fine detail
  - Fewer octaves = smoother, simpler patterns

- **scale**: Overall feature size (10.0-500.0)
  - Smaller scale = more frequent, smaller features
  - Larger scale = less frequent, larger features

- **persistence**: Amplitude reduction per octave (0.1-0.9)
  - Higher = more detail retained
  - Lower = smoother, less detail

- **lacunarity**: Frequency increase per octave (1.5-4.0)
  - Higher = more variation between octaves
  - Lower = more uniform detail

## Relating to Minecraft Datapacks

The noise patterns visualized here correspond to datapack elements:

### Java Edition

```json
{
  "type": "minecraft:noise",
  "noise": "minecraft:continentalness",
  "xz_scale": 1.0,  // Similar to our 'scale' parameter
  "y_scale": 1.0
}
```

### Visualization Mapping

| Visualization | Minecraft Datapack Element |
|---------------|---------------------------|
| Continentalness | `minecraft:continentalness` noise |
| Erosion | `minecraft:erosion` noise |
| Ridges | `minecraft:ridge` noise |
| Boulder Noise | Your custom noise in `density_function/` |
| Combined | Result of `minecraft:add` or `minecraft:mul` |

### Practical Application

1. **Visualize first**: Use this tool to see how your noise looks
2. **Tune parameters**: Adjust octaves, scale, persistence
3. **Implement in datapack**: Transfer settings to JSON
4. **Test in-game**: Load datapack and generate new chunks

## Examples and Tips

### Example 1: Testing Different Seeds

```bash
# Generate multiple visualizations with different seeds
for seed in 12345 67890 11111 99999; do
    python visualize_noise.py --seed $seed --output "terrain_seed_${seed}.png"
done
```

This creates multiple files showing how terrain varies with seed.

### Example 2: Boulder Density Tuning

Edit the boulder noise parameters in `visualize_noise.py`:

```python
# More frequent, smaller boulders
boulder_noise = visualizer.generate_perlin_noise(
    octaves=2, scale=20.0, persistence=0.3
)

# Less frequent, larger boulders  
boulder_noise = visualizer.generate_perlin_noise(
    octaves=4, scale=50.0, persistence=0.6
)
```

Then visualize to see the difference.

### Example 3: Matching Minecraft Terrain

To approximate specific Minecraft terrain types:

```python
# Plains-like (smooth, low variation)
plains = visualizer.generate_perlin_noise(octaves=3, scale=150.0)

# Mountains-like (rough, high variation)
mountains = visualizer.generate_perlin_noise(octaves=6, scale=80.0)

# Desert-like (medium smooth)
desert = visualizer.generate_perlin_noise(octaves=4, scale=120.0)
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError`:

```bash
pip install --upgrade numpy matplotlib noise
```

### Slow Generation

For faster generation:
- Reduce `--size` (try 64 or 32)
- Reduce octaves in the code
- Close other applications

### Memory Issues

If you run out of memory:
- Use smaller `--size` values
- Generate one noise type at a time
- Close the interactive display between runs

## Further Reading

- [Minecraft Wiki - Noise Generator](https://minecraft.wiki/w/Noise_generator)
- [Perlin Noise Explanation](https://en.wikipedia.org/wiki/Perlin_noise)
- [EXTENDING_NOISE_PATTERNS.md](../EXTENDING_NOISE_PATTERNS.md) - Main documentation

## Contributing

Feel free to:
- Add new noise pattern presets
- Create additional visualization styles
- Improve performance
- Add more Minecraft-accurate noise simulations

---

**Note**: These visualizations are approximations of Minecraft's noise system for learning purposes. Actual in-game terrain may differ due to Minecraft's specific noise implementation and additional generation steps.
