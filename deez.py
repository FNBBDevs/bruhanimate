"""
Here is a simple program that uses the EffectRenderer to render out one
of the prebuilt effects to the terminal.
"""
from bruhscreen import WinScreen
from bruhrenderer import *

# Define a function that the screen warpper function will call
def render_stars(screen, frames, time, effect, background, transparent):
    
    # Create the renderer
    renderer = EffectRenderer(screen, frames, time, effect, background, transparent)
    
    # Change the exit messages if you want, wipe tells the renderer to wipe the final
    # animation frame before displaying the exit messages.
    renderer.set_exit_stats("  Animation Frames Completed  ", "    Press [Enter] to leave    ", wipe=True)
    
    # Set the intensity if you want, the higher the intensity, the more stars.
    # Intensity can be set for the Noise and Stars Effect, 200 is a good spot.
    renderer.effect.update_intensity(200)
    
    # Run the animation
    renderer.run()
    
    # Add an input() to catch the end of the enimation
    input()

# Now that we have a funciton to render the animation, let's
# create a screen and call the function
#              function            fram  time  effect   bk   img
WinScreen.show(render_stars, args=(100, 0.05, "stars", " ", None))