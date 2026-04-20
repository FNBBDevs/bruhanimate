Settings
========

Every effect in ``bruheffect`` is configured through a settings dataclass. Construct
a settings object, populate only the fields you care about (all have defaults), and
pass it to the effect constructor. Settings can also be omitted entirely — each
effect falls back to its own defaults.

.. code-block:: python

   from bruhanimate import EffectRenderer, Screen, SnowSettings

   def demo(screen):
       renderer = EffectRenderer(screen, float("inf"), 0.05, "snow", " ", False)
       renderer.effect.set_wind(0.6)          # runtime setter
       renderer.run()

   Screen.show(demo)

.. automodule:: bruhanimate.bruheffect.settings
   :members:
   :undoc-members:
   :show-inheritance:
