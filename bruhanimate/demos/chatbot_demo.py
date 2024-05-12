import openai
from bruhanimate.bruhffer import Buffer
from bruhanimate.bruhscreen import Screen
from bruhanimate.bruhrenderer import EffectRenderer
from bruhanimate.bruheffects import SnowEffect


def chatbot(screen: Screen, openai_api_key: str):
    renderer = EffectRenderer(
        screen=screen,
        frames=float("inf"),
        time=0.03,
        effect_type="chat",
        background=" ",
        transparent=False,
    )
    renderer.effect.set_chatbot_print_halt(1)
    client = openai.OpenAI(
        api_key=openai_api_key
    )
    renderer.effect.set_chatbot_properties(
        interface="openai", model="gpt-3.5-turbo", user="Ethan", client=client
    )
    renderer.effect.set_avatar_properties(size=10)
    renderer.effect.set_chatbot_user_colors(
        chatbot_text_color=255,
        chatbot_background_color=None,
        chatbot_avatar_color=54,
        user_text_color=27,
        user_background_color=None,
        user_avatar_color=203,
    )
    renderer.effect.set_gradient_noise_halts(char_halt=1, color_halt=1)
    renderer.effect.set_chatbot_blink_halt(20)
    renderer.effect.set_chatbot_cursor_colors(255, 232)
    renderer.effect.set_divider_flag(True, divider_character=" ")
    chat_effect = SnowEffect(
        buffer=Buffer(screen.height, screen.width), background=" "
    )
    chat_effect.set_matrix_properties((1, 25), (1, 10), 0.5, 0.5, 0.5, 10)
    renderer.effect.set_second_effect(chat_effect)
    renderer.run()

def run(openai_api_key: str):
    Screen.show(chatbot, args=(openai_api_key))

if __name__ == "__main__":
    run()
