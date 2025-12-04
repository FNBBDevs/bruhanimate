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

import json
import math
import random
import string
from threading import Thread

import openai
import requests
from bruhcolor import bruhcolored

from ..bruhutil import Buffer, Screen
from .base_effect import BaseEffect


class Key:
    """
    A class representing a key on the keyboard with its position and value.
    """

    def __init__(
        self, character: str, representation: list[str], value: int, x: int, y: int
    ):
        """
        Initializes a Key object with the given parameters.

        Args:
            character (str): The character represented by the key.
            representation (list[str]): The visual representation of the key.
            value (int): The value of the key.
            x (int): The x-coordinate of the key on the screen.
            y (int): The y-coordinate of the key on the screen.
        """
        self.x = x
        self.y = y
        self.character = character
        self.representation = representation
        self.value = value

    def __str__(self):
        return self.character

    def __repr__(self):
        return self.character


class GradientNoise:
    """
    A class representing a noise effect with a color gradient.
    """

    def __init__(
        self,
        x: int,
        y: int,
        length: int,
        char_halt: int = 1,
        color_halt: int = 1,
        gradient_length: int = 1,
    ):
        """
        Initializes a GradientNoise object with the given parameters.

        Args:
            x (int): The x-coordinate of the noise effect on the screen.
            y (int): The y-coordinate of the noise effect on the screen.
            length (int): The length of the noise effect on the screen.
            char_halt (int, optional): The halt of characters changing (frame_number % character_halt == 0). Defaults to 1.
            color_halt (int, optional): The halt of colors changing (frame_number % color_halt == 0). Defaults to 1.
            gradient_length (int, optional): Length of the gradient. Defaults to 1.
        """
        self.x = x
        self.y = y
        self.__gradient_length = gradient_length
        # colors to use for gradient
        self.__gradient = [
            c
            for c in [
                232,
                232,
                232,
                232,
                233,
                233,
                233,
                233,
                234,
                234,
                234,
                234,
                235,
                235,
                235,
                235,
                236,
                236,
                236,
                236,
                237,
                238,
                239,
                240,
                241,
                242,
                243,
                244,
                245,
                246,
                247,
                248,
                249,
                250,
                251,
                252,
                253,
                254,
                255,
            ]
            for _ in range(self.__gradient_length)
        ]
        # delay to changing the chars in the noise
        self.__char_halt = char_halt
        self.__char_frame_number = 0
        # delay to change the gradient shift
        self.__color_halt = color_halt
        self.__color_frame_number = 0
        self.length = length
        self.done_generating = False

        self.string_chars = [" " for _ in range(self.length)]
        self.string_colors = [
            self.__gradient[i % len(self.__gradient)] for i in range(self.length)
        ]
        self.colored_chars = [
            bruhcolored(c, color=color)
            for c, color in zip(self.string_chars, self.string_colors)
        ]

    # change the gradient
    def update_gradient(self, gradient: list[int]):
        """
        Updates the gradient of the noise.

        Args:
            gradient (list[int]): The new gradient to use.
        """
        self.__gradient = [c for c in gradient for _ in range(self.__gradient_length)]
        return self

    def generate(self, frame_number: int):
        """
        Generates the next frame of the noise.

        Args:
            frame_number (int): The current frame number.
        """
        if self.done_generating:
            return
        # is it time to change the noise chars?
        if frame_number % self.__char_halt == 0:
            self.__char_frame_number += 1
            for i, c in enumerate(self.string_chars):
                # frame == 0 basically
                if not c:
                    self.string_chars[i] = random.choice(
                        string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/"
                    )
                # randomly decide to update this char to a new one
                elif random.random() < 0.6:
                    self.string_chars[i] = random.choice(
                        string.ascii_letters + "1234567890!@#$%^&*()_+-=<>,.:\";'{}[]?/"
                    )
        # is it time to change the gradient position?
        if frame_number % self.__color_halt == 0:
            self.__color_frame_number += 1
            self.string_colors = [
                self.__gradient[(i - self.__color_frame_number) % len(self.__gradient)]
                for i in range(self.length)
            ]

        # update the color characters exposed to the main program
        self.colored_chars = [
            bruhcolored(c, color=color)
            for c, color in zip(self.string_chars, self.string_colors)
        ]

    def mark_done(self):
        self.done_generating = True


class Loading:
    """
    A class to handle the loading animation.
    """

    def __init__(self, animate_part: GradientNoise):
        self.animate_part = animate_part

    def update(self, frame: int):
        self.animate_part.generate(frame)

    def mark_done(self):
        self.animate_part.mark_done()


class StringStreamer:
    """
    A class to handle the string streamer animation.
    """

    def __init__(self, x: int, y: int, text: str, start_frame: int, halt: int = 1):
        """
        Initialize the StringStreamer class.

        Args:
            x (int): The x position of the string streamer.
            y (int): The y position of the string streamer.
            text (str): The text to be displayed.
            start_frame (int): The frame number to start the animation.
            halt (int, optional): Halt value to delay the animation (frame_number & halt == 0). Defaults to 1.
        """
        self.x = x
        self.y = y
        self.text = text
        self.__start_frame = start_frame
        self.__halt = halt
        self.__chars = list(self.text)
        self.elapsed = []
        self.complete = False

    def generate(self, frame: int):
        """
        Generate the string streamer animation for a given frame number.

        Args:
            frame (int): The current frame number.
        """
        if self.complete or frame < self.__start_frame:
            return
        if frame % self.__halt == 0:
            self.elapsed.append(self.__chars[len(self.elapsed)])
            if len(self.elapsed) == len(self.__chars):
                self.complete = True


class OllamaApiCaller:
    """
    A class to interact with the Ollama API.
    """

    def __init__(
        self,
        model: str,
        use_message_history: bool = False,
        message_history_cap: int = 5,
    ):
        """
        Initialize the OllamaApiCaller class.

        Args:
            model (str): The Ollama model to use.
            use_message_history (bool, optional): Whether or not to use message history. Defaults to False.
            message_history_cap (int, optional): How many messages should we use, sliding window. Defaults to 5.
        """
        self.model = model
        self.url = "http://127.0.0.1:11434/api/chat"
        self.busy = False
        self.response = None
        self.state = "ready"
        self.use_message_history = use_message_history
        self.message_history = []
        self.message_history_cap = message_history_cap

    def chat(
        self, message: str, user: str | None, previous_messages: list[str] | None = None
    ) -> str:
        """
        Send a chat message to the Ollama API and get a response.

        Args:
            message (str): The message to send.
            user (str | None): The user who sent the message.
            previous_messages (list[str] | None, optional): Past sent messages. Defaults to None.

        Returns:
            str: Response from ollama.
        """
        self.busy = True
        self.state = "running"
        payload = {
            "model": self.model,
            "messages": (
                [{"role": "user", "content": message}]
                if not self.message_history
                else self.message_history + [{"role": "user", "content": message}]
            ),
            "stream": False,
        }

        response = requests.post(url=self.url, data=json.dumps(payload))

        self.response = response.json()["message"]["content"]
        self.busy = False
        self.state = "finished"

        if self.use_message_history:
            self.message_history += [
                {"role": "user", "content": message},
                {"role": "assistant", "content": self.response},
            ]
            if len(self.message_history) > self.message_history_cap:
                self.message_history_cap = self.message_history_cap[1:]


class OpenAiCaller:
    """
    Class to interact with the OpenAI API using the `openai` Python package.
    """

    def __init__(
        self,
        client: openai.OpenAI | openai.AzureOpenAI,
        model: str,
        use_message_history: bool = False,
        message_history_cap: int = 5,
    ):
        """
        Initialize the OpenAiCaller class.

        Args:
            client (openai.OpenAI | openai.AzureOpenAI): The OpenAI client object.
            model (str): The OpenAI model to be used.
            use_message_history (bool, optional): Whether or not to use message history. Defaults to False.
            message_history_cap (int, optional): Amount of messages from history to use, sliding window. Defaults to 5.
        """
        self.client = client
        self.model = model
        self.busy = False
        self.response = None
        self.state = "ready"
        self.use_message_history = use_message_history
        self.message_history = []
        self.message_history_cap = message_history_cap

    def chat(self, message: str, user: str | None) -> str:
        """
        Send a chat message to the OpenAI API and get a response.

        Args:
            message (str): The message to be sent to the OpenAI API.
            user (str | None): The user who sent the message.

        Returns:
            str: The response from the OpenAI API.
        """
        self.busy = True
        self.state = "running"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=(
                [{"role": "user", "content": message}]
                if not self.message_history
                else self.message_history + [{"role": "user", "content": message}]
            ),
            max_tokens=500,
            temperature=0.5,
        )

        self.response = response.choices[0].message.content
        self.busy = False
        self.state = "finished"

        if self.use_message_history:
            self.message_history += [
                {"role": "user", "content": message},
                {"role": "system", "content": self.response},
            ]
            if len(self.message_history) > self.message_history_cap:
                self.message_history_cap = self.message_history_cap[
                    len(self.message_history) - self.message_history_cap :
                ]


class ChatbotEffect(BaseEffect):
    """
    A class to create a chatbot effect.
    """

    def __init__(
        self, screen: Screen, buffer: Buffer, back_buffer: Buffer, background: str = " "
    ):
        """
        Initialize the ChatbotEffect class.

        Args:
            screen (Screen): Our instance of the terminal window
            buffer (Buffer): Effect buffer to push updates to.
            back_buffer (Buffer): The buffer to push the effect updates to.
            background (str, optional): Character or string to use for the background. Defaults to " ".
        """
        super(ChatbotEffect, self).__init__(buffer, background)
        self.back_buffer = back_buffer
        self.screen = screen
        self.turn = 0
        self.interface = None
        self.model = None
        self.chatbot = None
        self.show_stats = False
        self.last_chatbot_response = ""
        self.last_chatbot_response_words = []

        # manages how the buffer is updated . . .
        self.all_keys = {idx: [] for idx in range(screen.height)}
        self.last_key = None
        self.user_message = ""

        self.second_effect = None
        self.chat_thread = None
        self.chatbot_thinker = None
        self.total_processed_chatbot_words = 0
        self.current_chatbot_response_words_idx = 0
        self.chatbot_print_halt = 25
        self.global_current_y_idx = 0

        self.avatar_size = 10

        self.user_y_turn_start_idx = 0
        self.chat_y_turn_start_idx = 0
        self.current_top_y = 0
        self.current_bottom_y = self.screen.height - 1

        self.user_cursor_x_idx = self.avatar_size
        self.user_cursor_y_idx = 0

        # colors
        self.chatbot_text_color = 243
        self.chatbot_background_color = None
        self.user_text_color = 255
        self.user_background_color = None
        self.user_avatar_color = None
        self.user_avatar_text_color = 255
        self.chatbot_avatar_color = None
        self.chatbot_avatar_text_color = 255

        self.gradient_noise_char_halt = 1
        self.gradient_noise_color_halt = 1
        self.blink_halt = 20
        self.blink_color_one = 255
        self.blink_color_two = 232
        self.cursor_char_color = 255

        self.divider = False
        self.divider_character = "-"

        self.gradient_text_color = [21, 57, 93, 129, 165, 201, 165, 129, 93, 57]
        self.gradient_idx = 1
        self.gradient_mul = 1

        for ydx in range(screen.height):
            for _ in range(self.avatar_size):
                self.all_keys[ydx] = [
                    Key(" ", [ord(" ")], ord(" "), x=_, y=ydx)
                    for _ in range(self.avatar_size)
                ]

        self.message_history = []

        self.view_y_top = 0
        self.view_y_bottom = self.screen.height - 1
        self.avatar_placed = False

    def __expand_list(self, original_list: list[int | str], n: int, mul: int = 1):
        """
        Expands a list by adding `n` elements to the end of it, each multiplied by `mul`.

        Args:
            original_list (list[int | str]): The list to be expanded.
            n (int): The number of elements to add to the end of the list.
            mul (int, optional): The multiplier for each added element. Defaults to 1.
        Returns:
            _type_: _description_
        """
        l = []
        for val in original_list:
            for _ in range(mul):
                l.append(val)
        v = math.ceil(n / len(l))
        new_list = l * v
        return new_list[:n]

    def set_chatbot_properties(
        self,
        interface: str | None,
        model: str,
        user: str | None = None,
        client: openai.OpenAI | openai.AzureOpenAI | None = None,
        use_message_history: bool = False,
        message_history_cap: int = 5,
    ):
        """
        Sets the properties for the chatbot.

        Args:
            interface (str | None): The interface type, e.g., "OpenAI" or "Azure OpenAI".
            model (str): The name of the AI model to use.
            user (str | None, optional): The name of the user. Defaults to None.
            client (openai.OpenAI | openai.AzureOpenAI | None, optional): The client to use. Defaults to None.
            use_message_history (bool, optional): Whether or not to use message history. Defaults to False.
            message_history_cap (int, optional): How many messages from history to use, sliding window. Defaults to 5.

        Raises:
            Exception: If the interface is not recognized, an exception will be raised.
        """
        if interface:
            self.interface = interface
        if user:
            self.user = user
        self.model = model
        if interface == "ollama":
            self.chatbot = OllamaApiCaller(
                model=self.model,
                use_message_history=use_message_history,
                message_history_cap=message_history_cap,
            )
        elif interface == "openai":
            if not client:
                raise Exception(
                    "An OpenAI client object must be provided for interface of type 'openai'."
                )
            self.chatbot = OpenAiCaller(
                client=client,
                model=model,
                use_message_history=use_message_history,
                message_history_cap=message_history_cap,
            )

    def set_second_effect(self, effect: str):
        """
        Sets the second effect for the chatbot.

        Args:
            effect (str): The effect to use
        """
        self.second_effect = effect

    def set_chatbot_print_halt(self, halt: int):
        """
        Sets the chatbot print halt value to control how often it prints messages.

        Args:
            halt (int): (frame_number % halt == 0)
        """
        self.chatbot_print_halt = halt

    def set_gradient_noise_halts(
        self, char_halt: int | None = None, color_halt: int | None = None
    ):
        """
        Sets the gradient noise halts for character and color shifts.

        Args:
            char_halt (int | None, optional): Sets the character halt for gradient noise. Defaults to None.
            color_halt (int | None, optional): Sets the color halt for gradient noise. Defaults to None.
        """
        if char_halt:
            self.gradient_noise_char_halt = char_halt
        if color_halt:
            self.gradient_noise_color_halt = color_halt

    def set_chatbot_user_colors(
        self,
        chatbot_text_color: int | str | None = None,
        chatbot_background_color: int | str | None = None,
        chatbot_avatar_color: int | str | None = None,
        chatbot_avatar_text_color: int | str | None = None,
        user_text_color: int | str | None = None,
        user_background_color: int | str | None = None,
        user_avatar_color: int | str | None = None,
        user_avatar_text_color: int | str | None = None,
    ):
        """
        Sets the colors for the chatbot and user messages.

        Args:
            chatbot_text_color (int | str | None, optional): Color of chatbot output text. Defaults to None.
            chatbot_background_color (int | str | None, optional): Background of chatbot output text. Defaults to None.
            chatbot_avatar_color (int | str | None, optional): Text color of avatar logo. Defaults to None.
            chatbot_avatar_text_color (int | str | None, optional): Background color of avatar logo. Defaults to None.
            user_text_color (int | str | None, optional): Color of user text. Defaults to None.
            user_background_color (int | str | None, optional): Background color of user text. Defaults to None.
            user_avatar_color (int | str | None, optional): Text color of user avatar. Defaults to None.
            user_avatar_text_color (int | str | None, optional): Background color of user avatar. Defaults to None.
        """
        if chatbot_text_color:
            self.chatbot_text_color = chatbot_text_color
        if chatbot_background_color:
            self.chatbot_background_color = chatbot_background_color
        if chatbot_avatar_color:
            self.chatbot_avatar_color = chatbot_avatar_color
        if chatbot_avatar_text_color:
            self.chatbot_avatar_text_color = chatbot_avatar_text_color
        if user_text_color:
            self.user_text_color = user_text_color
        if user_background_color:
            self.user_background_color = user_background_color
        if user_avatar_color:
            self.user_avatar_color = user_avatar_color
        if user_avatar_text_color:
            self.user_avatar_text_color = user_avatar_text_color

    def set_avatar_properties(self, size: int):
        """
        Set avatar properties for user and chatbot.

        Args:
            size (int): Length of the avatars on left side of screen.
        """
        self.avatar_size = size
        self.user_cursor_x_idx = self.avatar_size
        for ydx in range(self.screen.height):
            self.all_keys[ydx] = [
                Key(" ", [ord(" ")], ord(" "), x=_, y=ydx)
                for _ in range(self.avatar_size)
            ]

    def set_chatbot_stats(self, show: bool = False):
        """
        Set chatbot stats on the right side of screen.

        Args:
            show (bool, optional): Whether or not to show chatbot stats. Defaults to False.
        """
        self.show_stats = show

    def set_chatbot_blink_halt(self, halt: int):
        """
        Set chatbot blink and halt properties.

        Args:
            halt (int): (frame_number % halt == 0)
        """
        self.blink_halt = halt

    def set_divider_flag(self, divider: bool, divider_character: str = "-"):
        """
        Set the divider flag and character for screen.

        Args:
            divider (bool): Whether or not to show the divider.
            divider_character (str, optional): Character to use for the divider. Defaults to "-".
        """
        self.divider = divider
        self.divider_character = divider_character

    def set_chatbot_cursor_colors(self, color_one: int | str, color_two: int | str):
        """
        Set the colors for chatbot cursor.

        Args:
            color_one (int | str): First color of cursor.
            color_two (int | str): Second color of cursor.
        """
        self.blink_color_one = color_one
        self.blink_color_two = color_two

    def set_chatbot_text_gradient(self, gradient: list[int | str], mul: int):
        """
        Set the text color for chatbot to use a gradient.

        Args:
            gradient (list[int | str]): Gradient color to use for chatbot loading.
            mul (int): Multiplier for the gradient effect.
        """
        self.gradient_text_color = gradient
        self.gradient_mul = mul

    def __handle_keyboard_result(self, result: int):
        """
        Handle the keyboard input and return a result.

        Args:
            result (int): Result from pressing down keyboard from win32 package.

        Returns:
            bool: Something . . .
        """
        if result:
            if result == -300:  # backspace
                if self.user_cursor_x_idx == self.avatar_size:
                    return
                all_key_history = self.all_keys[self.user_cursor_y_idx]
                if all_key_history == []:
                    if self.user_cursor_y_idx - 1 >= self.global_current_y_idx:
                        self.user_cursor_y_idx -= 1
                        if self.user_cursor_y_idx in self.all_keys:
                            keys = self.all_keys[self.user_cursor_y_idx]
                            if keys:
                                self.user_cursor_x_idx = self.all_keys[
                                    self.user_cursor_y_idx
                                ][-1].x
                            else:
                                self.user_cursor_x_idx = 0
                        else:
                            self.user_cursor_x_idx = 0
                else:
                    last_key = all_key_history[-1]
                    self.user_cursor_x_idx -= len(last_key.representation)
                    self.all_keys[self.user_cursor_y_idx] = all_key_history[:-1]
                if self.user_cursor_y_idx < 0:
                    self.user_cursor_y_idx = 0
                if len(self.user_message) > 0:
                    self.user_message = self.user_message[:-1]
                return False
            elif result == 10:  # enter
                self.user_cursor_y_idx += 1
                if self.user_cursor_y_idx >= max(self.all_keys):
                    self.scroll_keys(shift=1)
                self.user_cursor_x_idx = self.avatar_size
                return self.last_key != "\\"
            elif result == 11:  # tab
                self.user_cursor_x_idx += 4
                self.all_keys[self.user_cursor_y_idx].append(
                    Key(
                        character=" ",
                        representation=[32, 32, 32, 32],
                        value=result,
                        x=self.user_cursor_x_idx,
                        y=self.user_cursor_y_idx,
                    )
                )
                return False
            elif result == -204:  # arrow up
                if self.current_top_y != 0:
                    self.current_top_y -= 1
                    self.current_bottom_y -= 1
            elif result == -206:  # arrow down
                if self.current_bottom_y < (len(self.all_keys) - 1):
                    self.current_top_y += 1
                    self.current_bottom_y += 1
            elif result > 0:
                self.user_cursor_x_idx += 1
                self.all_keys[self.user_cursor_y_idx].append(
                    Key(
                        character=bruhcolored(
                            text=chr(result),
                            color=self.user_text_color,
                            on_color=self.user_background_color,
                        ).colored,
                        representation=[result],
                        value=result,
                        x=self.user_cursor_x_idx,
                        y=self.user_cursor_y_idx,
                    )
                )
                self.last_key = chr(result)
                self.user_message += chr(result)
                return False

    def __scroll_up(self):
        """
        Scroll up the display by one line.
        """
        first_key = min(self.all_keys.keys())
        last_key = max(self.all_keys.keys())
        if len(self.all_keys) == 0 or first_key == 0:
            return
        for key in range(first_key, last_key):
            self.all_keys[key] = self.all_keys[key + 1]
        self.all_keys[last_key] = [
            Key(" ", [ord(" ")], ord(" "), x=_, y=last_key)
            for _ in range(self.avatar_size)
        ]

        if self.current_top_y > 0:
            self.current_top_y = self.current_top_y - 1
            self.current_bottom_y = self.current_bottom_y - 1

    def __scroll_down(self):
        """
        Scroll down the display by one line.
        """
        last_key = max(self.all_keys.keys())
        self.all_keys[last_key + 1] = [
            Key(" ", [ord(" ")], ord(" "), x=_, y=last_key + 1)
            for _ in range(self.avatar_size)
        ]
        # if len(self.all_keys) >= 100:
        #     first_key = min(self.all_keys.keys())
        #     del self.all_keys[first_key]
        #     self.all_keys = {k-1:v for k,v in self.all_keys.items()}
        # else:
        self.current_top_y = self.current_top_y + 1
        self.current_bottom_y = self.current_bottom_y + 1
        self.all_keys = {
            i: self.all_keys[key] for i, key in enumerate(sorted(self.all_keys.keys()))
        }

    def scroll_keys(self, shift: int = 1):
        """
        Scroll the keys up or down by one line

        Args:
            shift (int, optional): How much to scroll. Defaults to 1.
        """
        self.__scroll_down() if shift == 1 else self.__scroll_up()

    def place_all_keys(self):
        """
        Place all keys on to the buffer.
        """
        for idx, vals in self.all_keys.items():
            if idx > self.current_bottom_y or idx < self.current_top_y:
                continue
            displacement = 0
            for jdx, key in enumerate(vals):
                if len(key.representation) > 1:
                    for val in key.representation:
                        self.buffer.put_char(
                            jdx + displacement, idx - self.current_top_y, chr(val)
                        )
                        displacement += 1
                    displacement -= 1
                else:
                    self.buffer.put_char(
                        jdx + displacement, idx - self.current_top_y, key.character
                    )

    def render_frame(self, frame_number: int):
        """
        Render the current state of the buffer to the terminal.

        Args:
            frame_number (int): The frame number to render.
        """
        self.buffer.clear_buffer()
        if self.turn == 0:
            if not self.avatar_placed:
                for i, c in enumerate(self.user[: self.avatar_size - 1]):
                    self.all_keys[self.user_y_turn_start_idx][i] = Key(
                        bruhcolored(
                            c,
                            color=self.user_avatar_text_color,
                            on_color=self.user_avatar_color,
                        ).colored,
                        [ord(c)],
                        ord(c),
                        None,
                        None,
                    )
                for i in range(len(self.user), self.avatar_size - 1):
                    self.all_keys[self.user_y_turn_start_idx][i] = Key(
                        bruhcolored(" ", on_color=self.user_avatar_color).colored,
                        [ord(" ")],
                        ord(" "),
                        None,
                        None,
                    )
                self.avatar_placed = True
            self.screen.wait_for_input(timeout=0)
            result = self.screen.get_event()
            flip_turn = self.__handle_keyboard_result(result=result)
            if flip_turn:
                self.avatar_placed = False
                self.turn = 1
                if self.divider:
                    for _ in range(self.avatar_size):
                        self.all_keys[self.user_cursor_y_idx].append(
                            Key(
                                self.divider_character,
                                [ord(self.divider_character)],
                                ord(self.divider_character),
                                None,
                                None,
                            )
                        )
                    for _ in range(self.avatar_size, self.buffer.width()):
                        self.all_keys[self.user_cursor_y_idx].append(
                            Key(
                                self.divider_character,
                                [ord(self.divider_character)],
                                ord(self.divider_character),
                                None,
                                None,
                            )
                        )
                    self.user_cursor_y_idx += 1
                    if self.user_cursor_y_idx >= max(self.all_keys):
                        self.scroll_keys(shift=1)
                self.chat_y_turn_start_idx = self.user_cursor_y_idx
        else:
            # call llm with self.user_message
            if self.chatbot.state == "ready":
                message = self.user_message[:]
                self.thread = Thread(
                    target=self.chatbot.chat,
                    args=(
                        message,
                        self.user,
                    ),
                )
                self.thread.start()
                self.chatbot_thinker = GradientNoise(
                    x=0,
                    y=self.user_cursor_y_idx,
                    length=self.avatar_size - 1,
                    char_halt=self.gradient_noise_char_halt,
                    color_halt=self.gradient_noise_color_halt,
                    gradient_length=2,
                )  # .update_gradient([21, 57, 93, 129, 165, 201, 165, 129, 93, 57])
            elif (
                self.thread
                and not self.thread.is_alive()
                and self.chatbot.state == "finished"
            ):
                self.thread.join()
                self.thread = None
                if len(self.chatbot.response) > self.buffer.width():
                    self.last_chatbot_response = self.chatbot.response
                else:
                    self.last_chatbot_response = self.chatbot.response
                self.last_chatbot_response_words = self.last_chatbot_response.split(" ")
                self.chatbot.response = ""
                self.user_message = ""
                self.chatbot.state = "printing"
                if self.chatbot_text_color == "gradient":
                    self.gradient_idx = 1
                    self.gradient_text_color_for_message = self.__expand_list(
                        self.gradient_text_color, len(self.last_chatbot_response), 3
                    )
            elif self.chatbot.state == "printing":
                # print out the characters!
                if not self.avatar_placed:
                    for i, c in enumerate(self.model[: self.avatar_size - 1]):
                        self.all_keys[self.chat_y_turn_start_idx][i] = Key(
                            bruhcolored(
                                c,
                                color=self.chatbot_avatar_text_color,
                                on_color=self.chatbot_avatar_color,
                            ).colored,
                            [ord(c)],
                            ord(c),
                            None,
                            None,
                        )
                    for i in range(len(self.model), self.avatar_size - 1):
                        self.all_keys[self.chat_y_turn_start_idx][i] = Key(
                            bruhcolored(
                                " ", on_color=self.chatbot_avatar_color
                            ).colored,
                            [ord(" ")],
                            ord(" "),
                            None,
                            None,
                        )
                    self.avatar_placed = True
                if frame_number & self.chatbot_print_halt == 0:
                    if self.total_processed_chatbot_words == len(
                        self.last_chatbot_response_words
                    ):
                        self.chatbot.state = "done"
                        self.current_chatbot_response_words_idx = 0
                        self.total_processed_chatbot_words = 0
                    else:
                        next_word = (
                            self.last_chatbot_response_words[
                                self.current_chatbot_response_words_idx
                            ]
                            + " "
                        )
                        for idx, character in enumerate(next_word):
                            if self.user_cursor_y_idx >= max(self.all_keys):
                                self.scroll_keys(shift=1)
                            if character == "\n":
                                self.user_cursor_y_idx += 1
                                if self.user_cursor_y_idx >= max(self.all_keys):
                                    self.scroll_keys(shift=1)
                                self.all_keys[self.user_cursor_y_idx][
                                    self.avatar_size - 2
                                ] = Key(
                                    character=">",
                                    representation=[ord(">")],
                                    value=ord(">"),
                                    x=None,
                                    y=None,
                                )
                                continue
                            self.all_keys[self.user_cursor_y_idx].append(
                                Key(
                                    character=bruhcolored(
                                        text=character,
                                        color=self.chatbot_text_color
                                        if self.chatbot_text_color != "gradient"
                                        else self.gradient_text_color_for_message[
                                            self.gradient_idx - 1
                                        ],
                                        on_color=self.chatbot_background_color,
                                    ).colored,
                                    representation=[ord(character)],
                                    value=ord(character),
                                    x=self.user_cursor_x_idx,
                                    y=self.user_cursor_y_idx,
                                )
                            )
                            if character != " ":
                                self.gradient_idx += 1
                            if (
                                len(self.all_keys[self.user_cursor_y_idx])
                                == self.buffer.width()
                            ):
                                self.user_cursor_y_idx += 1
                                if self.user_cursor_y_idx >= max(self.all_keys):
                                    self.scroll_keys(shift=1)
                                self.all_keys[self.user_cursor_y_idx][
                                    self.avatar_size - 2
                                ] = Key(
                                    character=">",
                                    representation=[ord(">")],
                                    value=ord(">"),
                                    x=None,
                                    y=None,
                                )
                        self.current_chatbot_response_words_idx += 1
                        self.total_processed_chatbot_words += 1
            elif self.chatbot.state == "done":
                self.turn = 0
                self.avatar_placed = False
                self.chatbot_thinker = None
                self.chatbot.state = "ready"
                self.global_current_y_idx += 1
                if self.divider:
                    self.user_cursor_y_idx += 1
                    if self.user_cursor_y_idx >= max(self.all_keys):
                        self.scroll_keys(shift=1)
                    for _ in range(self.avatar_size):
                        self.all_keys[self.user_cursor_y_idx].append(
                            Key(
                                self.divider_character,
                                [ord(self.divider_character)],
                                ord(self.divider_character),
                                None,
                                None,
                            )
                        )
                    for _ in range(self.avatar_size, self.buffer.width()):
                        self.all_keys[self.user_cursor_y_idx].append(
                            Key(
                                self.divider_character,
                                [ord(self.divider_character)],
                                ord(self.divider_character),
                                None,
                                None,
                            )
                        )
                self.user_cursor_y_idx += 1
                if self.user_cursor_y_idx >= max(self.all_keys):
                    self.scroll_keys(shift=1)
                self.user_y_turn_start_idx = self.user_cursor_y_idx
            else:
                self.chatbot_thinker.generate(frame_number=frame_number)

        if self.second_effect:
            self.second_effect.render_frame(frame_number=frame_number)
            self.buffer.sync_with(self.second_effect.buffer)

        self.place_all_keys()

        if self.chatbot_thinker and self.chatbot.state == "running":
            for i, c in enumerate(self.chatbot_thinker.colored_chars):
                self.buffer.put_char(
                    self.chatbot_thinker.x + i, self.chatbot_thinker.y, c.colored
                )

        if self.show_stats:
            self.buffer.put_at(
                0,
                self.buffer.height() - 5,
                f"CURSOR X: {self.user_cursor_x_idx}",
                transparent=True,
            )
            self.buffer.put_at(
                0,
                self.buffer.height() - 4,
                f"CURSOR Y: {self.user_cursor_y_idx}",
                transparent=True,
            )
            self.buffer.put_at(
                0,
                self.buffer.height() - 3,
                f"CHATBOT STATE: {self.chatbot.state}",
                transparent=True,
            )
            self.buffer.put_at(
                0,
                self.buffer.height() - 2,
                f"CHATBOT RESPONSE WORD COUNT: {0 if not self.last_chatbot_response_words else len(self.last_chatbot_response_words)}",
                transparent=True,
            )
            self.buffer.put_at(
                0,
                self.buffer.height() - 1,
                f"PROCESSED RESPONSE WORDS: {self.total_processed_chatbot_words}",
                transparent=True,
            )

        if self.turn == 0:
            if frame_number % self.blink_halt == 0:
                self.cursor_char_color = (
                    self.blink_color_one
                    if self.cursor_char_color == self.blink_color_two
                    else self.blink_color_two
                )
            self.buffer.put_char(
                self.user_cursor_x_idx,
                self.user_cursor_y_idx,
                bruhcolored(" ", on_color=self.cursor_char_color).colored,
                transparent=False,
            )
