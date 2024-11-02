"""
Copyright 2023 Ethan Christensen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from ..bruhrenderer import CenterRenderer
from ..bruhutil import Screen, text_to_image, get_image

def fireworks(screen: Screen):
    renderer = CenterRenderer(
        screen=screen,
        img=text_to_image("FIREWORKS!"),
        frames=float("inf"),
        frame_time=0.05,
        effect_type="firework",
        background=" ",
        transparent=False
    )

    renderer.effect.set_firework_rate(firework_rate=0.1)
    renderer.effect.set_firework_color_enabled(True)
    renderer.effect.set_firework_color_type("solid")
    renderer.effect.set_firework_type("random")
    
    renderer.run()

def run():
    Screen.show(fireworks)

if __name__ == "__main__":
    run()
