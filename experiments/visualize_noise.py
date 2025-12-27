#!/usr/bin/env python3
"""
Minecraft Noise Pattern Visualizer

This script generates 2D and 3D visualizations of Minecraft-style noise patterns
to help understand how different noise configurations affect terrain generation.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from noise import pnoise2, snoise2
import argparse


class MinecraftNoiseVisualizer:
    """Visualize Minecraft-style noise patterns in 2D and 3D."""
    
    def __init__(self, seed=12345, size=128):
        """
        Initialize the noise visualizer.
        
        Args:
            seed: Random seed for reproducible noise generation
            size: Size of the noise map (size x size grid)
        """
        self.seed = seed
        self.size = size
        np.random.seed(seed)
        
    def generate_perlin_noise(self, octaves=4, persistence=0.5, lacunarity=2.0, scale=50.0):
        """
        Generate Perlin noise similar to Minecraft's terrain generation.
        
        Args:
            octaves: Number of noise layers (more = more detail)
            persistence: Amplitude multiplier per octave
            lacunarity: Frequency multiplier per octave
            scale: Overall scale of the noise
            
        Returns:
            2D numpy array of noise values
        """
        noise_map = np.zeros((self.size, self.size))
        
        for i in range(self.size):
            for j in range(self.size):
                noise_map[i][j] = pnoise2(
                    i / scale,
                    j / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=self.seed
                )
        
        return noise_map
    
    def generate_simplex_noise(self, octaves=4, persistence=0.5, lacunarity=2.0, scale=50.0):
        """
        Generate Simplex noise (used in modern Minecraft versions).
        
        Args:
            octaves: Number of noise layers
            persistence: Amplitude multiplier per octave
            lacunarity: Frequency multiplier per octave
            scale: Overall scale of the noise
            
        Returns:
            2D numpy array of noise values
        """
        noise_map = np.zeros((self.size, self.size))
        
        for octave in range(octaves):
            freq = lacunarity ** octave
            amp = persistence ** octave
            
            for i in range(self.size):
                for j in range(self.size):
                    noise_map[i][j] += snoise2(
                        (i / scale) * freq + self.seed,
                        (j / scale) * freq + self.seed
                    ) * amp
        
        return noise_map
    
    def generate_continentalness(self):
        """
        Simulate Minecraft's continentalness noise (controls landmass).
        Low frequency, large-scale terrain variation.
        """
        return self.generate_perlin_noise(octaves=6, scale=200.0, persistence=0.6)
    
    def generate_erosion(self):
        """
        Simulate Minecraft's erosion noise (controls terrain smoothness).
        Medium frequency noise.
        """
        return self.generate_perlin_noise(octaves=5, scale=80.0, persistence=0.5)
    
    def generate_ridges(self):
        """
        Simulate Minecraft's ridge noise (creates mountain ridges).
        Uses absolute values to create sharp peaks.
        """
        noise = self.generate_perlin_noise(octaves=4, scale=60.0, persistence=0.5)
        return 1.0 - np.abs(noise)  # Invert and abs to create ridges
    
    def combine_noise_patterns(self, base_noise, added_noise, blend_factor=0.5):
        """
        Combine two noise patterns (like adding boulder noise to terrain).
        
        Args:
            base_noise: Base terrain noise
            added_noise: Additional feature noise
            blend_factor: How much to blend (0.0 to 1.0)
            
        Returns:
            Combined noise map
        """
        return base_noise + added_noise * blend_factor
    
    def visualize_2d(self, noise_map, title="Noise Pattern", cmap='terrain'):
        """
        Create a 2D heatmap visualization of the noise.
        
        Args:
            noise_map: 2D array of noise values
            title: Plot title
            cmap: Matplotlib colormap
        """
        plt.figure(figsize=(10, 8))
        plt.imshow(noise_map, cmap=cmap, interpolation='bilinear')
        plt.colorbar(label='Noise Value')
        plt.title(f'{title} (Seed: {self.seed})')
        plt.xlabel('X Coordinate')
        plt.ylabel('Z Coordinate')
        return plt
    
    def visualize_3d(self, noise_map, title="Noise Pattern 3D", cmap='terrain'):
        """
        Create a 3D surface plot of the noise.
        
        Args:
            noise_map: 2D array of noise values
            title: Plot title
            cmap: Matplotlib colormap
        """
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create meshgrid for plotting
        x = np.arange(0, self.size, 1)
        z = np.arange(0, self.size, 1)
        X, Z = np.meshgrid(x, z)
        
        # Plot surface
        surf = ax.plot_surface(X, Z, noise_map, cmap=cmap, 
                              linewidth=0, antialiased=True, alpha=0.9)
        
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Z Coordinate')
        ax.set_zlabel('Noise Value (Height)')
        ax.set_title(f'{title} (Seed: {self.seed})')
        
        # Add colorbar
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
        # Set viewing angle
        ax.view_init(elev=30, azim=45)
        
        return plt
    
    def visualize_comparison(self, noise_maps, titles, output_file=None):
        """
        Create a comparison plot showing multiple noise patterns.
        
        Args:
            noise_maps: List of 2D noise arrays
            titles: List of titles for each noise map
            output_file: Optional filename to save the plot
        """
        n_maps = len(noise_maps)
        fig, axes = plt.subplots(2, n_maps, figsize=(5*n_maps, 10))
        
        if n_maps == 1:
            axes = axes.reshape(-1, 1)
        
        for idx, (noise_map, title) in enumerate(zip(noise_maps, titles)):
            # 2D view
            im = axes[0, idx].imshow(noise_map, cmap='terrain', interpolation='bilinear')
            axes[0, idx].set_title(f'{title}\n(2D View)')
            axes[0, idx].set_xlabel('X')
            axes[0, idx].set_ylabel('Z')
            plt.colorbar(im, ax=axes[0, idx])
            
            # 3D-style contour view
            levels = np.linspace(noise_map.min(), noise_map.max(), 15)
            contour = axes[1, idx].contourf(noise_map, levels=levels, cmap='terrain')
            axes[1, idx].set_title(f'{title}\n(Contour View)')
            axes[1, idx].set_xlabel('X')
            axes[1, idx].set_ylabel('Z')
            plt.colorbar(contour, ax=axes[1, idx])
        
        fig.suptitle(f'Minecraft Noise Pattern Comparison (Seed: {self.seed})', 
                     fontsize=16, y=0.995)
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            print(f"Saved comparison plot to {output_file}")
        
        return plt


def main():
    """Main function with example visualizations."""
    parser = argparse.ArgumentParser(
        description='Visualize Minecraft-style noise patterns for terrain generation'
    )
    parser.add_argument('--seed', type=int, default=12345,
                       help='Random seed for noise generation')
    parser.add_argument('--size', type=int, default=128,
                       help='Size of the noise map (default: 128)')
    parser.add_argument('--output', type=str, default='noise_comparison.png',
                       help='Output filename for the comparison plot')
    parser.add_argument('--show', action='store_true',
                       help='Display plots interactively')
    
    args = parser.parse_args()
    
    # Create visualizer
    visualizer = MinecraftNoiseVisualizer(seed=args.seed, size=args.size)
    
    print(f"Generating noise patterns with seed {args.seed}...")
    
    # Generate different noise types
    print("  - Generating continentalness (base terrain)...")
    continentalness = visualizer.generate_continentalness()
    
    print("  - Generating erosion (terrain smoothness)...")
    erosion = visualizer.generate_erosion()
    
    print("  - Generating ridges (mountain peaks)...")
    ridges = visualizer.generate_ridges()
    
    print("  - Generating boulder noise (custom feature)...")
    boulder_noise = visualizer.generate_perlin_noise(
        octaves=3, scale=30.0, persistence=0.4
    )
    
    print("  - Combining base terrain with boulder placement...")
    combined = visualizer.combine_noise_patterns(
        continentalness, boulder_noise, blend_factor=0.3
    )
    
    # Create comparison visualization
    noise_maps = [
        continentalness,
        erosion,
        ridges,
        boulder_noise,
        combined
    ]
    
    titles = [
        'Continentalness\n(Base Terrain)',
        'Erosion\n(Terrain Smoothness)',
        'Ridges\n(Mountain Peaks)',
        'Boulder Noise\n(Custom Feature)',
        'Combined\n(Terrain + Boulders)'
    ]
    
    print(f"Creating visualization...")
    visualizer.visualize_comparison(noise_maps, titles, output_file=args.output)
    
    print(f"\n✓ Visualization complete!")
    print(f"  Output saved to: {args.output}")
    
    if args.show:
        print("  Displaying plot...")
        plt.show()
    else:
        print("  (Use --show flag to display interactively)")
    
    # Example: Create individual 3D plot for combined terrain
    if args.show:
        print("\nGenerating 3D visualization of combined terrain...")
        visualizer.visualize_3d(combined, "Combined Terrain + Boulders (3D)")
        plt.show()


if __name__ == '__main__':
    main()
