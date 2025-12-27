#!/usr/bin/env python3
"""
Example: Custom Noise Pattern for Boulder Placement

This example shows how to create and visualize a custom noise pattern
that could be used for terrain-aware boulder placement in Minecraft.
"""

from visualize_noise import MinecraftNoiseVisualizer
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Create visualizer with a specific seed for reproducibility
    seed = 42
    visualizer = MinecraftNoiseVisualizer(seed=seed, size=128)
    
    print(f"Creating custom boulder placement visualization (seed: {seed})...")
    
    # 1. Generate base terrain (like Minecraft's continentalness)
    print("  Generating base terrain...")
    base_terrain = visualizer.generate_continentalness()
    
    # 2. Generate custom boulder noise pattern
    # Smaller scale = boulders appear in clusters
    # Fewer octaves = smoother distribution
    print("  Generating boulder distribution pattern...")
    boulder_pattern = visualizer.generate_perlin_noise(
        octaves=3,
        scale=40.0,
        persistence=0.4,
        lacunarity=2.0
    )
    
    # 3. Create terrain-scaled boulder placement
    # This makes boulders more likely in mountainous areas
    print("  Scaling boulders based on terrain height...")
    # Normalize base terrain to 0-1 range
    terrain_normalized = (base_terrain - base_terrain.min()) / (base_terrain.max() - base_terrain.min())
    
    # Multiply boulder pattern by terrain height (more boulders in mountains)
    terrain_aware_boulders = boulder_pattern * terrain_normalized
    
    # 4. Create threshold visualization (simulates noise_threshold_count)
    # In Minecraft, you might use: "above_threshold": 0.3
    threshold = 0.2
    boulder_placement_mask = (terrain_aware_boulders > threshold).astype(float)
    
    # 5. Visualize the results
    print("  Creating comparison visualization...")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Plot 1: Base Terrain
    im1 = axes[0, 0].imshow(base_terrain, cmap='terrain', interpolation='bilinear')
    axes[0, 0].set_title('Base Terrain\n(Continentalness)')
    axes[0, 0].set_xlabel('X')
    axes[0, 0].set_ylabel('Z')
    plt.colorbar(im1, ax=axes[0, 0])
    
    # Plot 2: Raw Boulder Noise
    im2 = axes[0, 1].imshow(boulder_pattern, cmap='YlOrBr', interpolation='bilinear')
    axes[0, 1].set_title('Boulder Noise Pattern\n(Raw)')
    axes[0, 1].set_xlabel('X')
    axes[0, 1].set_ylabel('Z')
    plt.colorbar(im2, ax=axes[0, 1])
    
    # Plot 3: Terrain-Aware Boulder Noise
    im3 = axes[0, 2].imshow(terrain_aware_boulders, cmap='YlOrBr', interpolation='bilinear')
    axes[0, 2].set_title('Terrain-Aware Boulders\n(Scaled by Height)')
    axes[0, 2].set_xlabel('X')
    axes[0, 2].set_ylabel('Z')
    plt.colorbar(im3, ax=axes[0, 2])
    
    # Plot 4: Boulder Placement Mask (Above Threshold)
    im4 = axes[1, 0].imshow(boulder_placement_mask, cmap='Greys', interpolation='nearest')
    axes[1, 0].set_title(f'Boulder Placement\n(Threshold > {threshold})')
    axes[1, 0].set_xlabel('X')
    axes[1, 0].set_ylabel('Z')
    plt.colorbar(im4, ax=axes[1, 0])
    
    # Plot 5: Overlay on Terrain
    # Show terrain with boulder locations
    overlay = axes[1, 1].imshow(base_terrain, cmap='terrain', alpha=0.7)
    axes[1, 1].contour(boulder_placement_mask, levels=[0.5], colors='red', linewidths=2)
    axes[1, 1].set_title('Boulders on Terrain\n(Red = Boulder Locations)')
    axes[1, 1].set_xlabel('X')
    axes[1, 1].set_ylabel('Z')
    plt.colorbar(overlay, ax=axes[1, 1])
    
    # Plot 6: Density Heatmap
    # Count boulders in regions
    kernel_size = 8
    from scipy.ndimage import uniform_filter
    boulder_density = uniform_filter(boulder_placement_mask, size=kernel_size)
    im6 = axes[1, 2].imshow(boulder_density, cmap='hot', interpolation='bilinear')
    axes[1, 2].set_title('Boulder Density\n(Local Concentration)')
    axes[1, 2].set_xlabel('X')
    axes[1, 2].set_ylabel('Z')
    plt.colorbar(im6, ax=axes[1, 2])
    
    fig.suptitle(f'Custom Boulder Placement Example (Seed: {seed})', 
                 fontsize=16, y=0.995)
    plt.tight_layout()
    
    # Save the result
    output_file = 'example_boulder_placement.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\n✓ Visualization saved to: {output_file}")
    
    # Print statistics
    total_blocks = boulder_placement_mask.size
    boulder_blocks = np.sum(boulder_placement_mask)
    percentage = (boulder_blocks / total_blocks) * 100
    
    print(f"\nStatistics:")
    print(f"  Total area: {total_blocks} blocks")
    print(f"  Boulder locations: {int(boulder_blocks)} blocks")
    print(f"  Coverage: {percentage:.2f}%")
    print(f"  Avg terrain height: {base_terrain.mean():.3f}")
    print(f"  Max boulder density: {boulder_density.max():.3f}")
    
    print("\nThis pattern could be implemented in Minecraft using:")
    print("  - Java Edition: noise_threshold_count with continentalness")
    print("  - Bedrock Edition: scatter_feature with q.noise() and q.heightmap()")


if __name__ == '__main__':
    try:
        from scipy.ndimage import uniform_filter
    except ImportError:
        print("Installing scipy for density calculation...")
        import subprocess
        subprocess.check_call(['pip', 'install', '-q', 'scipy'])
        from scipy.ndimage import uniform_filter
    
    main()
