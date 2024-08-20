# bruhanimate
[![Downloads](https://static.pepy.tech/badge/bruhanimate)](https://pepy.tech/project/bruhanimate)
[![Downloads](https://static.pepy.tech/badge/bruhanimate/month)](https://pepy.tech/project/bruhanimate)
[![Downloads](https://static.pepy.tech/badge/bruhanimate/week)](https://pepy.tech/project/bruhanimate)
<div>
<img src="https://i.ibb.co/TwssymP/BRUHANIMA.gif" alt="BRUHANIMA" border="0">

<img src="https://i.ibb.co/p3mbKb1/plas.gif" alt="plas" border="0">

<img src="https://i.ibb.co/pR49kL6/noises.gif" alt="noises" border="0">
</div>

[![Supported Python versions](https://img.shields.io/pypi/pyversions/termcolor.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/bruhanimate/)

bruhanimate offers a series of files to aid in rendering out animations in the terminal. This is heavily inspisred by the <a href="https://github.com/peterbrittain/asciimatics">Asciimatics</a> package. While Asciimatics is the end-all be-all for termianl animations, I figured it would be good practice to go ahead and attempt something like this myself.

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

# Quick Start
Use some of the built in demos to see what is possible. There are demos for each effect. Simply import `<effect>_demo` from bruhanimate and call the `<effect>_demo.run()` to run the demo!
- static
- offset
- noise
- stars
- snow
- rain
- plasma
- gol (Conway's Game of Life)
- matrix
- twinkle

```py
# Import a demo
from bruhanimate import plasma_demo
# run the demo
plasma_demo.run()
```

# Usage
Here are some examples on how bruhanimate might be used. <br/><br/>

Pass in arguments through the `show()` command. <br/>
```py

"""
Here is a simple program that uses the EffectRenderer passing in
the arguments to the main function
"""
from bruhanimate import Screen, CenterRenderer, images


def demo(screen, img, frames, time, effect_type, background, transparent):
    renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)
    renderer.update_smart_transparent(True)
    renderer.effect.update_color(True)
    renderer.effect.update_intensity(100)
    renderer.run()


def main():
    Screen.show(demo, args=(images.get_image("TWOPOINT"), 300, 0, "noise", " ", False))


if __name__ == "__main__":
    main()
```

Set the arguments directly in the function invoked by `show()`. <br/>
```py
"""
Here is a simple program that uses the EffectRenderer setting the arguments
directly in the main function.
"""
from bruhanimate import Screen, EffectRenderer


def demo(screen: Screen):
    renderer = EffectRenderer(
        screen=screen,
        frames=float("inf"),
        time=0.1,
        effect_type="snow",
        background=" ",
        transparent=False
    )
    renderer.run()


if __name__ == "__main__":
    Screen.show(main)
```