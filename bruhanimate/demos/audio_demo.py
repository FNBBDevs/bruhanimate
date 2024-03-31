from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import CenterRenderer
import bruhanimate.images as images
from bruhanimate.bruheffects import _GRADIENTS

import os
os.system(" ")


def audio(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=images.text_to_image("AUDIO!"),
        time=0.0,
        effect_type="audio",
        background=" ",
        transparent=False,
    )
    renderer.effect.set_audio_properties(num_bands=screen.width, audio_halt=1, use_gradient=True)
    renderer.effect.set_audio_gradient(_GRADIENTS[0], mode="repeat")
    renderer.effect.set_orientation("top")
    renderer.run()


def run():
    Screen.show(audio)


if __name__ == "__main__":
    run()
