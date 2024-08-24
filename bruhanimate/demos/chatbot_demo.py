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

import os
import openai
os.system(" ")

from bruhanimate import Buffer, Screen
from bruhanimate import EffectRenderer
from bruhanimate import TwinkleEffect


def chatbot(screen: Screen, openai_api_key: str, name: str):
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
        interface="openai", model="gpt-3.5-turbo", user=name, client=client
    )
    renderer.effect.set_avatar_properties(size=10)
    renderer.effect.set_chatbot_user_colors(
        chatbot_text_color=255,
        chatbot_background_color=None,
        chatbot_avatar_color=235,
        chatbot_avatar_text_color=255,
        user_text_color=255,
        user_background_color=None,
        user_avatar_color=255,
        user_avatar_text_color=232
    )
    renderer.effect.set_gradient_noise_halts(char_halt=1, color_halt=1)
    renderer.effect.set_chatbot_blink_halt(20)
    renderer.effect.set_chatbot_cursor_colors(255, 232)
    renderer.effect.set_divider_flag(True, divider_character=" ")
    chat_effect = TwinkleEffect(
        buffer=Buffer(screen.height, screen.width), background=" "
    )
    renderer.effect.set_second_effect(chat_effect)
    renderer.run()

def run(openai_api_key: str, name: str = "User"):
    Screen.show(chatbot, args=(openai_api_key, name,))

if __name__ == "__main__":
    run()
