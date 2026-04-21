# bruhanimate
[![Downloads](https://static.pepy.tech/badge/bruhanimate)](https://pepy.tech/project/bruhanimate)
[![Downloads](https://static.pepy.tech/badge/bruhanimate/month)](https://pepy.tech/project/bruhanimate)
[![Downloads](https://static.pepy.tech/badge/bruhanimate/week)](https://pepy.tech/project/bruhanimate)
<div>
<img src="https://github.com/user-attachments/assets/22d61f3e-b3ca-406f-9e1c-2f539eea23c7" alt="snow" border="0">
<img src="https://github.com/user-attachments/assets/644afa91-ffb0-465e-815f-998a59759c3b" alt="fireworks" border="0">
</div>

[![Supported Python versions](https://img.shields.io/pypi/pyversions/termcolor.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/bruhanimate/)

bruhanimate provides a set of tools for creating and rendering animations directly in the terminal. Designed for ease of use, this package enables developers to incorporate dynamic animations into command-line applications. While drawing inspiration from existing terminal animation libraries, bruhanimate brings a fresh approach and offers a unique set of features tailored for flexibility and creativity in terminal-based projects.

Inspired by the <a href="https://github.com/peterbrittain/asciimatics">Asciimatics</a> package.

## Installation

### From PyPI

```bash
pip install --upgrade bruhanimate
```

### From source

```bash
git clone https://github.com/FNBBDevs/bruhanimate
cd bruhanimate
python -m pip install .
```

## Quick Start

Use the built-in demos to explore each effect. Each demo can be run two ways:

**From Python:**
```python
from bruhanimate import plasma_demo
plasma_demo.run()
```

**From the command line:**
```bash
python -m bruhanimate.demos.plasma_demo
```

Available demos: `static_demo`, `offset_demo`, `noise_demo`, `stars_demo`, `snow_demo`, `rain_demo`, `plasma_demo`, `gol_demo`, `matrix_demo`, `twinkle_demo`, `firework_demo`, `fire_demo`, `julia_demo`, `line_demo`, `audio_demo`, `boids_demo`, `sand_demo`, `diffusion_demo`, `automaton_demo`, `voronoi_demo`, `perlin_demo`, `holiday`.

## Effects

Every effect is configured through a **settings object** — one dataclass per effect, all fields optional with sensible defaults. Pass it to the effect at construction time, or leave it out to get the defaults.

| Effect | Settings class | Key options |
|---|---|---|
| `StaticEffect` | — | none |
| `OffsetEffect` | `OffsetSettings` | `direction` |
| `NoiseEffect` | `NoiseSettings` | `intensity`, `color` |
| `StarEffect` | `StarSettings` | `color_type` |
| `SnowEffect` | `SnowSettings` | `intensity`, `wind`, `show_info`, `collision` |
| `RainEffect` | `RainSettings` | `intensity`, `wind_direction`, `swells`, `collision` |
| `PlasmaEffect` | `PlasmaSettings` | `color`, `characters`, `random_colors`, `show_info` |
| `MatrixEffect` | `MatrixSettings` | `character_halt_range`, `color_halt_range`, randomness, `gradient_length` |
| `GameOfLifeEffect` | `GameOfLifeSettings` | `decay`, `color`, `color_type`, `scale` |
| `TwinkleEffect` | `TwinkleSettings` | `twinkle_chars`, `density` |
| `FireEffect` | `FireSettings` | `intensity`, `wind_direction`, `wind_strength`, `use_char_color`, `swell`, `turbulence` |
| `FireworkEffect` | `FireworkSettings` | `firework_type`, `color_enabled`, `color_type`, `rate` |
| `JuliaEffect` | — | none |
| `DrawLinesEffect` | `DrawLinesSettings` | `char`, `thin` |
| `BoidsEffect` | `BoidsSettings` | `num_boids`, `color`, `char`, `max_speed`, `perception` |
| `SandEffect` | `SandSettings` | `color`, `char`, `spawn_rate` |
| `DiffusionEffect` | `DiffusionSettings` | `color`, `char`, `f`, `k`, `steps_per_frame` |
| `AutomatonEffect` | `AutomatonSettings` | `color`, `char`, `rule` |
| `VoronoiEffect` | `VoronoiSettings` | `color`, `char`, `num_seeds`, `seed_speed` |
| `PerlinEffect` | `PerlinSettings` | `color`, `char`, `octaves`, `speed`, `threshold` |

## Usage

### Basic — defaults

```python
from bruhanimate import Screen, EffectRenderer

def demo(screen: Screen):
    renderer = EffectRenderer(
        screen=screen,
        frames=float("inf"),
        frame_time=0.05,
        effect_type="snow",
        background=" ",
        transparent=False,
    )
    renderer.run()

if __name__ == "__main__":
    Screen.show(demo)
```

### With settings

```python
from bruhanimate import Screen, EffectRenderer, SnowSettings, SnowEffect

def demo(screen: Screen):
    renderer = EffectRenderer(
        screen=screen,
        frames=float("inf"),
        frame_time=0.05,
        effect_type="snow",
        background=" ",
        transparent=False,
    )
    # configure via settings at construction
    renderer.effect = SnowEffect(
        renderer.effect.buffer,
        " ",
        settings=SnowSettings(intensity=0.01, wind=0.6),
    )
    renderer.run()

if __name__ == "__main__":
    Screen.show(demo)
```

### Runtime setters

Settings configure the effect at construction. All effects also expose `set_*` methods for changes mid-animation:

```python
renderer.effect.set_wind(0.8)          # SnowEffect
renderer.effect.set_intensity(0.4)     # FireEffect
renderer.effect.set_wind_direction("east")  # RainEffect
renderer.effect.set_color_properties(color=True, random_colors=True)  # PlasmaEffect
renderer.effect.shuffle_plasma_values()
```

### Effect Registry

Every built-in effect is registered in `effect_registry` — a discoverable, extensible registry that maps effect names to their class, settings class, description, and named presets.

```python
from bruhanimate import effect_registry

# List all registered effects
for name, entry in effect_registry.entries().items():
    print(name, "—", entry.description)

# List presets for an effect
print(effect_registry.presets("snow"))
# {'light': SnowSettings(...), 'moderate': SnowSettings(...), 'blizzard': SnowSettings(...), 'windy': SnowSettings(...)}

# Create an effect by name with a preset
effect = effect_registry.create("snow", buffer, " ", preset="blizzard")

# Create an effect with a custom settings object
from bruhanimate import SnowSettings
effect = effect_registry.create("snow", buffer, " ", settings=SnowSettings(wind=0.8))

# Register your own effect
from bruhanimate import EffectRegistry
effect_registry.register(
    "myeffect",
    MyEffect,
    settings_cls=MySettings,
    description="Does something cool",
    presets={"fast": MySettings(speed=10)},
)
```

Available built-in presets:

| Effect | Presets |
|---|---|
| `offset` | `right`, `left`, `up`, `down` |
| `noise` | `sparse`, `dense`, `color` |
| `stars` | `greyscale`, `color` |
| `plasma` | `greyscale`, `color`, `blocks`, `random` |
| `gol` | `plain`, `decay`, `color` |
| `rain` | `drizzle`, `storm`, `monsoon` |
| `matrix` | `default`, `fast` |
| `drawlines` | `thin`, `thick` |
| `snow` | `light`, `moderate`, `blizzard`, `windy` |
| `twinkle` | `sparse`, `dense` |
| `firework` | `plain`, `color`, `random` |
| `fire` | `campfire`, `inferno`, `windy` |
| `audio` | `bars`, `mirror`, `waveform`, `minimal` |

### Renderers

| Renderer | Description |
|---|---|
| `EffectRenderer` | Full-screen effect |
| `CenterRenderer` | Effect with a centered image overlay |
| `PanRenderer` | Effect with a panning image |
| `FocusRenderer` | Effect with a focused/zooming image |
| `BackgroundColorRenderer` | Solid background color |

```python
from bruhanimate import Screen, CenterRenderer, bruhimage

def demo(screen: Screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=300,
        frame_time=1/30,
        img=bruhimage.text_to_image("RAIN!", padding_top_bottom=1, padding_left_right=2),
        effect_type="rain",
        background=" ",
        transparent=False,
    )
    renderer.update_collision(True)
    renderer.effect.set_swells(True)
    renderer.effect.set_wind_direction("east")
    renderer.run()

if __name__ == "__main__":
    Screen.show(demo)
```
