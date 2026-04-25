# bruhanimate
[![Downloads](https://static.pepy.tech/badge/bruhanimate)](https://pepy.tech/project/bruhanimate)
[![Downloads](https://static.pepy.tech/badge/bruhanimate/month)](https://pepy.tech/project/bruhanimate)
[![Downloads](https://static.pepy.tech/badge/bruhanimate/week)](https://pepy.tech/project/bruhanimate)
<div>
<img src="https://github.com/user-attachments/assets/22d61f3e-b3ca-406f-9e1c-2f539eea23c7" alt="snow" border="0">
<img src="https://github.com/user-attachments/assets/644afa91-ffb0-465e-815f-998a59759c3b" alt="fireworks" border="0">
</div>

[![Supported Python versions](https://img.shields.io/pypi/pyversions/bruhanimate.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/bruhanimate/)

**bruhanimate** is a high-performance ASCII terminal animation package for Python. It provides a rich set of tools for creating dynamic, interactive, and visually stunning animations directly in your command-line interface.

Inspired by [Asciimatics](https://github.com/peterbrittain/asciimatics), bruhanimate offers a streamlined architecture built around Buffers, Effects, and Renderers, making it easy to create everything from simple falling snow to complex fractal animations and real-time audio visualizers.

---

## Features

- **20+ Built-in Effects:** From classic Matrix rain to organic Reaction-Diffusion patterns.
- **Flexible Rendering:** Multiple renderer types for full-screen effects, centered images, panning backgrounds, and interactive terminals.
- **System Audio Visualization:** Real-time visualizers with 25+ different display modes.
- **Easy Customization:** Configure effects via typed settings classes or named presets.
- **Image & Text Support:** Convert images and text (via PyFiglet) to ASCII for use in animations.
- **Cross-Platform:** Works on Windows, macOS, and Linux.

---

## Installation

### From PyPI

```bash
pip install --upgrade bruhanimate
```

### With Audio Support
To use the `AudioEffect`, you'll need the optional audio dependencies:
```bash
pip install "bruhanimate[audio]"
```

### From Source
```bash
git clone https://github.com/FNBBDevs/bruhanimate
cd bruhanimate
pip install .
```

---

## Quick Start

The best way to see what **bruhanimate** can do is to run the built-in demos:

**From the command line:**
```bash
python -m bruhanimate.demos.plasma_demo
```

**From Python:**
```python
from bruhanimate import plasma_demo
plasma_demo.run()
```

**Available demos:** `static`, `offset`, `noise`, `stars`, `snow`, `rain`, `plasma`, `gol`, `matrix`, `twinkle`, `firework`, `fire`, `julia`, `line`, `audio`, `boids`, `sand`, `diffusion`, `automaton`, `voronoi`, `perlin`, `holiday`.

---

## How it Works: The Architecture

bruhanimate uses a layered approach to rendering:

1.  **Screen:** Handles the terminal window, input events, and final output.
2.  **Buffer:** A 2D grid of characters and colors. Effects draw into a Buffer.
3.  **Effect:** Logic that updates a Buffer every frame (e.g., moving "snowflakes" down).
4.  **Renderer:** Coordinates the Screen and the Effect. It can overlay images, handle transparency, and manage the animation loop.

---

## Effects Registry

Every effect in bruhanimate is registered in the `effect_registry`. You can discover effects, their descriptions, and their available presets at runtime.

| Effect | Description | Key Settings |
|---|---|---|
| `StaticEffect` | Fills screen with a static character. | — |
| `OffsetEffect` | Scrolling background in any direction. | `direction` |
| `NoiseEffect` | Random "TV static" pixels. | `intensity`, `color` |
| `StarEffect` | Twinkling star field. | `color_type` |
| `SnowEffect` | Falling snow with accumulation and wind. | `intensity`, `wind`, `collision` |
| `RainEffect` | Falling rain with lightning and swells. | `intensity`, `wind_direction`, `lightning` |
| `PlasmaEffect` | Animated sine-wave plasma. | `color`, `characters`, `random_colors` |
| `MatrixEffect` | Cascading digital rain. | `gradient_length`, `randomness` |
| `GameOfLifeEffect` | Conway's Game of Life. | `decay`, `color`, `scale` |
| `TwinkleEffect` | Characters that pulse in brightness. | `density`, `twinkle_chars` |
| `FireworkEffect` | Exploding fireworks (45+ types). | `firework_type`, `color_type`, `rate` |
| `FireEffect` | Particle-based fire simulation. | `intensity`, `wind`, `turbulence` |
| `JuliaEffect` | Animated Julia-set fractal. | — |
| `WaterEffect` | Rippling water surface. | — |
| `BoidsEffect` | Flocking bird simulation. | `num_boids`, `max_speed`, `perception` |
| `SandEffect` | Falling-sand cellular automaton. | `spawn_rate`, `char`, `color` |
| `DiffusionEffect` | Organic reaction-diffusion patterns. | `f` (feed), `k` (kill), `steps_per_frame` |
| `AutomatonEffect` | 1D Elementary Cellular Automata (e.g. Rule 30). | `rule`, `char`, `color` |
| `VoronoiEffect` | Shifting Voronoi cells. | `num_seeds`, `seed_speed` |
| `PerlinEffect` | Smooth multi-octave noise field. | `octaves`, `speed`, `threshold` |
| `AudioEffect` | Real-time system audio visualizer. | `mode` (bars, wave, tunnel, etc.), `smoothing` |

### Using Presets
Most effects come with named presets for quick configuration:
```python
from bruhanimate import effect_registry

# Create a 'blizzard' snow effect
effect = effect_registry.create("snow", buffer, " ", preset="blizzard")
```

---

## Renderers

Renderers determine how the effect is presented on the screen.

| Renderer | Description |
|---|---|
| `EffectRenderer` | Basic full-screen animation. |
| `CenterRenderer` | Overlays a static image/text in the center of the effect. |
| `PanRenderer` | Pans an image across the background effect. |
| `FocusRenderer` | Zooms into/out of a centered image. |
| `TerminalRenderer` | **Interactive:** Provides a functional shell overlay on top of the animation. |
| `BackgroundColorRenderer` | A simple solid color background. |

---

## Usage Example: Custom Snow Animation

```python
from bruhanimate import Screen, EffectRenderer, SnowSettings, SnowEffect

def demo(screen: Screen):
    # Initialize the renderer
    renderer = EffectRenderer(
        screen=screen,
        frames=float("inf"),
        frame_time=0.05,
        effect_type="snow",
        background=" ",
        transparent=False,
    )
    
    # Customize the effect via settings
    renderer.effect = SnowEffect(
        renderer.effect.buffer,
        " ",
        settings=SnowSettings(intensity=0.02, wind=0.5, collision=True),
    )
    
    # Start the animation
    renderer.run()

if __name__ == "__main__":
    Screen.show(demo)
```

---

## Utilities

- **`bruhimage`:** Convert images to ASCII or generate ASCII text from fonts.
  - `text_to_image("HELLO", font="slant")`
  - `get_image("path/to/img.png")`
- **`Buffer`:** Manually manipulate the 2D grid.
  - `buffer.put_at(x, y, char, color)`
- **`Screen`:** Low-level terminal control.

---

## Documentation

For more detailed information, API references, and advanced tutorials, visit the official documentation:
[https://ethanlchristensen.github.io/bruhanimate/](https://ethanlchristensen.github.io/bruhanimate/)

---

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
