# bruhanimate
bruhanimate offers a series of files to aid in rendering out animations in the terminal. This is heavily inspisred by the <a href="https://github.com/peterbrittain/asciimatics">Asciimatics</a> package. While this package does everyething you would want one to do, I figured it would be good practice to go ahead and attempt something like this myself.

# Usage
This is no where near complete, but does offer the ability to render out static images in the center of the screen. This would look something like this . . . <br/><br/>
```py

"""
Here is a simple program that uses the CenterRenderer to render out a static
ASCII image in the center of the terminal
"""
from bruhscreen import WinScreen
from bruhrenderer import CenterRenderer

# Create a simple ASCII image
img = [
    f"    __  __          ",
    f"   / / / /__  __  __",
    f"  / /_/ / _ \/ / / /",
    f" / __  /  __/ /_/ / ",
    f"/_/ /_/\___/\__, /  ",
    f"           /____/   "
]

# Define a function to handle the animation
# This is what we will wrap the screen in
def render(screen, frames, time, background, img):
    # Create the renderer
    renderer = CenterRenderer(screen, frames, time, background, img)
    # Edit the exit messages
    renderer.set_exit_stats(msg1=" Animation is Complete ", msg2=" Press [Enter] to Exit ", wipe=False)
    # Run the frames
    renderer.run()

# Create the screen and wrap it with the renderer
# note: this is similar to Asciimatics
WinScreen.wrapper(render, args=(20, 0.2, " ", img,))

# You can also render out the static animation without an image
# In this case, only the specified backgroudn character will be rendered
WinScreen.wrapper(render, args=(20, 0.2, " ", None,))

```
