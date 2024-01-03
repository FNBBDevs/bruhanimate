from bruhanimate.bruhrenderer import *
from bruhanimate.bruhscreen import Screen
import bruhanimate.images as images


def show(screen):
    try:
        image = images.text_to_image(
            "PLASMA!", padding_top_bottom=1, padding_left_right=3
        )

        # Create the renderer
        renderer = FocusRenderer(
            screen=screen,
            frames=500,
            time=0,
            img=image,
            effect_type="plasma",
            background=" ",
            transparent=False,
            start_frame=110,
            reverse=True,
            start_reverse=300,
        )

        # Set the attributes
        renderer.effect.update_color_properties(
            color=True, characters=True, random_color=True
        )

        renderer.effect.update_grey_scale_size(10)

        renderer.effect.update_plasma_values(10, 26, 19, 41)
        
        renderer.effect.update_info_visibility(True)

        # Run the animation
        renderer.update_exit_stats(
            "   Hey dude, the frames are done!   ",
            "        Press [Enter] to exit       ",
            wipe=True,
            centered=True,
        )
        renderer.run(end_message=True)

        # Catch the end with input() --> for Win-Systems --> no input() is needed for Unix-Systems
        input()

    except KeyboardInterrupt:
        renderer.render_exit()
        renderer.push_front_to_screen()
        input()


def run():
    Screen.show(show)


if __name__ == "__main__":
    run()
