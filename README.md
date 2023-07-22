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

# Usage
Here are some examples on how bruhanimate might be used. <br/><br/>
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

```py

"""
Here is another example that makes use of line drawing to draw a 3-D triangle
"""
from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images

def demo(screen, img, frames, time, effect, background, transparent):
    # CREATE THE RENDERER
    renderer = PanRenderer(screen, frames, time, img, effect, background, transparent, loop=True)
    
    # REGISTER THE LINES - LET'S MAKE A DECENT 3D TRIANGLE
    renderer.effect.add_line((15, 15), (30, 30))
    renderer.effect.add_line((30, 30), (50, 20))
    renderer.effect.add_line((50, 20), (15, 15))

    renderer.effect.add_line((30,30), (32, 22))
    renderer.effect.add_line((32, 22), (15, 15))
    renderer.effect.add_line((32, 22), (50, 20))


    # RUN THE ANIMATION
    renderer.run(end_message=False)

    # CATCH THE END WITH INPUT() ON WINDOWS
    input()

image = images.text_to_image("HELLO WORLD!", padding_top_bottom=1, padding_left_right=3)
Screen.show(demo, args=(image, 500, 0.05, "drawlines", " ", True))

```
