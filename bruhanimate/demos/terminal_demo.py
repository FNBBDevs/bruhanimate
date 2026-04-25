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

from bruhanimate.bruhrenderer import TerminalRenderer
from bruhanimate.bruhutil import Screen
from bruhanimate.bruhutil.utils import INF


def demo(screen, frames, time, effect, background, transparent):
    """
    Runs the terminal demo.
    """
    renderer = TerminalRenderer(
        screen,
        frames,
        time,
        effect,
        background,
        transparent,
    )

    renderer.update_smart_transparent(True)
    renderer.run()


def main():
    """
    Main function to run the TerminalRenderer demo.
    """
    # Using 'snow' as a nice, unintrusive background effect for a terminal
    Screen.show(demo, args=(INF, 0.05, "snow", " ", True))


if __name__ == "__main__":
    main()
