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

Use the built-in demos to explore each effect. Import any `<effect>_demo` from `bruhanimate` and call `.run()`.

```python
from bruhanimate import plasma_demo
plasma_demo.run()
```

Available demos: `static_demo`, `offset_demo`, `noise_demo`, `stars_demo`, `snow_demo`, `rain_demo`, `plasma_demo`, `gol_demo`, `matrix_demo`, `twinkle_demo`, `firework_demo`, `fire_demo`, `julia_demo`, `line_demo`, `holiday`.

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
