# bruhanimate

<img src="https://i.ibb.co/TwssymP/BRUHANIMA.gif" alt="BRUHANIMA" border="0">

<img src="https://i.ibb.co/PckYkGB/BRUHANIMATE-Made-with-Clipchamp.gif" alt="BRUHANIMATE-Made-with-Clipchamp" border="0">

[![Supported Python versions](https://img.shields.io/pypi/pyversions/termcolor.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/bruhanimate/)

bruhanimate offers a series of files to aid in rendering out animations in the terminal. This is heavily inspisred by the <a href="https://github.com/peterbrittain/asciimatics">Asciimatics</a> package. While Asciimatics is the end-all be-all for termianl animations, I figured it would be good practice to go ahead and attempt something like this myself.

## Installation

### From PyPI

```bash
python -m pip install --upgrade bruhanimate
```

### From source

```bash
git clone https://github.com/ethanlchristensen/bruhanimate
cd bruhanimate
python -m pip install .
```

# Usage
This is not complete, but currently offers the ability to render out background-effects. There also exists renderers that can render out images to the screen, but these need to be modified following the implementation of the `Effects` class. A great example of the effects can be found in `demo.py`. Here is a what a simple example might look like. <br/><br/>
```py

"""
Here is a simple program that uses the EffectRenderer to render out one
of the prebuilt effects to the terminal.
"""
from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images
import sys

def demo(screen, img, frames, time, effect_type, background, transparent):
    
    # CREATE THE RENDERER
    renderer = CenterRenderer(screen, frames, time, img, effect_type, background, transparent)

    # SET EFFECT ATTRIBUTES
    renderer.update_smart_transparent(True)
    renderer.effect.update_color(True)
    renderer.effect.update_intensity(100)

    # RUN THE ANIMATION
    renderer.run()

    # CATCH THE END WITH INPUT() --> for Win-Systems --> Ctl-C for Unix-Systems
    input()


def main():
    Screen.show(demo, args=(images.get_image("TWOPOINT"), 300, 0, "noise", " ", False))



if __name__ == "__main__":
    main()

```
