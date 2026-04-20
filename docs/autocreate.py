import os

# Define the components and their submodules
COMPONENTS = {
    "bruheffect": [
        "audio_effect",
        "base_effect",
        "chatbot_effect",
        "draw_lines_effect",
        "firework_effect",
        "game_of_life_effect",
        "matrix_effect",
        "noise_effect",
        "offset_effect",
        "plasma_effect",
        "rain_effect",
        "snow_effect",
        "star_effect",
        "static_effect",
        "twinkle_effect",
    ],
    "bruhrenderer": [
        "background_color_renderer",
        "base_renderer",
        "center_renderer",
        "effect_renderer",
        "focus_renderer",
        "pan_renderer",
    ],
    "bruhutil": [
        "bruherrors",
        "bruhffer",
        "bruhimage",
        "bruhscreen",
        "bruhtypes",
        "utils",
    ],
    "demos": [
        "audio_demo",
        "chatbot_demo",
        "firework_demo",
        "gol_demo",
        "holiday",
        "line_demo",
        "matrix_demo",
        "noise_demo",
        "offset_demo",
        "plasma_demo",
        "rain_demo",
        "snow_demo",
        "stars_demo",
        "static_demo",
        "twinkle_demo",
    ],
}

# Create directory structure and files
DOCS_DIR = os.path.join("docs", "source")

for component, modules in COMPONENTS.items():
    # Create component directory
    component_dir = os.path.join(DOCS_DIR, component)
    os.makedirs(component_dir, exist_ok=True)

    # Create index.rst
    index_content = f"""{component.capitalize()}
{"=" * len(component)}

This section contains content related to the {component} package.

.. toctree::
   :maxdepth: 2
   :caption: {component.capitalize()} Contents:

{chr(10).join("   " + module for module in modules)}

Overview
--------
Description of the {component} modules and their purposes...
"""
    with open(os.path.join(component_dir, "index.rst"), "w") as f:
        f.write(index_content)

    # Create individual module files
    for module in modules:
        title = " ".join(word.capitalize() for word in module.split("_"))
        content = f"""{title}
{"=" * len(title)}

.. automodule:: bruhanimate.{component}.{module}
   :members:
   :undoc-members:
   :show-inheritance:
"""
        with open(os.path.join(component_dir, f"{module}.rst"), "w") as f:
            f.write(content)

print("Documentation structure generated successfully!")
