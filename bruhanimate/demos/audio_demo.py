import os
os.system(" ")

from bruhanimate.bruhutil import Screen, images, GRADIENTS
from bruhrenderer import CenterRenderer
from bruhanimate import GRADIENTS


def audio(screen):
    renderer = CenterRenderer(
        screen=screen,
        frames=float("inf"),
        img=images.text_to_image("AUDIO!"),
        time=0.01,
        effect_type="audio",
        background=" ",
        transparent=False,
    )
    renderer.effect.set_audio_properties(num_bands=screen.width, audio_halt=15, use_gradient=True)
    renderer.effect.set_audio_gradient(GRADIENTS[0], mode="repeat")
    renderer.effect.set_orientation("top")
    renderer.run()


def run():
    Screen.show(audio)


if __name__ == "__main__":
    run()
