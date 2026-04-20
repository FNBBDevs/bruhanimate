Bruhanimate
===========

**bruhanimate** is a Python package for creating terminal animations. It provides a
collection of visual effects, a double-buffered rendering pipeline, and a simple
settings-based configuration system so you can tune every effect without touching
internal state.

Each effect is configured through a **settings dataclass**:

.. code-block:: python

   from bruhanimate import Screen, EffectRenderer, SnowSettings, SnowEffect

   def demo(screen):
       renderer = EffectRenderer(screen, float("inf"), 0.05, "snow", " ", False)
       # pass settings at construction time
       renderer.effect = SnowEffect(
           renderer.effect.buffer, " ",
           settings=SnowSettings(intensity=0.01, wind=0.5),
       )
       renderer.run()

   Screen.show(demo)

All effects also expose ``set_*`` methods for changes during a running animation:

.. code-block:: python

   renderer.effect.set_wind(0.8)
   renderer.effect.set_intensity(0.4)
   renderer.effect.set_color_properties(color=True, random_colors=True)

.. toctree::
   :maxdepth: 2
   :caption: Contents

   bruheffect/index
   bruhrenderer/index
   bruhutil/index
   demos/index
