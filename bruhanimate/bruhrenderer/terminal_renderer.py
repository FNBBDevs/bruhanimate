import os
import queue
import subprocess
import sys
import threading
import time
from typing import Any

from ..bruhutil import Screen
from ..bruhutil.bruherrors import ScreenResizedError
from ..bruhutil.bruhtypes import EffectType
from ..bruhutil.utils import sleep
from .base_renderer import BaseRenderer

INF = float("inf")


class TerminalRenderer(BaseRenderer):
    """
    An interactive Terminal Renderer with improved pipe handling and
    environment spoofing to better support interactive CLIs.
    """

    def __init__(
        self,
        screen: Screen,
        frames: int = 100,
        frame_time: float = 0.1,
        effect_type: EffectType = "static",
        background: str = " ",
        transparent: bool = False,
        collision: bool = False,
        settings: Any = None,
        preset: str | None = None,
    ):
        super().__init__(
            screen,
            frames,
            frame_time,
            effect_type,
            background,
            transparent,
            collision,
            settings=settings,
            preset=preset,
        )

        self.terminal_history = []
        self.current_line_output = ""
        self.current_input = ""
        self.prompt = "> "
        self.max_lines = self.height - 2
        self.output_queue = queue.Queue()
        self.active_process = None

    def _enqueue_output(self, out, queue):
        """Thread worker to read output character by character."""
        try:
            while True:
                char = out.read(1)
                if not char:
                    break
                queue.put(char)
            out.close()
        except Exception:
            pass

    def execute_command(self):
        """Starts a command or sends input to an active process."""
        user_text = self.current_input

        if self.active_process and self.active_process.poll() is None:
            self.terminal_history.append(user_text)
            try:
                # Use os.linesep to ensure the correct Enter key behavior for the OS
                self.active_process.stdin.write(user_text + os.linesep)
                self.active_process.stdin.flush()
            except Exception as e:
                self.terminal_history.append(f"[Stdin Error: {e}]")
            self.current_input = ""
            return

        self.terminal_history.append(self.prompt + user_text)
        self.current_input = ""

        cmd = user_text.strip()
        if not cmd:
            return

        if cmd.lower() in ("exit", "quit"):
            self.terminal_history.append("Type ESC to exit.")
            return

        try:
            # Spoof environment to trick some CLIs into working over pipes
            env = os.environ.copy()
            env["TERM"] = "xterm-256color"
            env["PYTHONUNBUFFERED"] = "1"
            env["FORCE_COLOR"] = "1"  # Try to force color support

            self.active_process = subprocess.Popen(
                cmd,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                env=env,
                universal_newlines=True,
            )

            threading.Thread(
                target=self._enqueue_output,
                args=(self.active_process.stdout, self.output_queue),
                daemon=True,
            ).start()
            threading.Thread(
                target=self._enqueue_output,
                args=(self.active_process.stderr, self.output_queue),
                daemon=True,
            ).start()

        except Exception as e:
            self.terminal_history.append(f"[Start Error: {e}]")

    def update_history_from_queue(self):
        """Assembles lines from characters in the queue."""
        while not self.output_queue.empty():
            try:
                char = self.output_queue.get_nowait()
                if char == "\n":
                    self.terminal_history.append(self.current_line_output)
                    self.current_line_output = ""
                elif char == "\r":
                    continue
                else:
                    self.current_line_output += char
                    if len(self.current_line_output) > self.width - 2:
                        self.terminal_history.append(self.current_line_output)
                        self.current_line_output = ""
            except queue.Empty:
                break

    def render_img_frame(self, frame_number):
        self.update_history_from_queue()
        self.image_buffer.clear_buffer(val=None)

        all_lines = list(self.terminal_history)
        if self.current_line_output:
            all_lines.append(self.current_line_output)

        display_lines = all_lines[-(self.max_lines - 1) :] if all_lines else []

        y_offset = 1
        for line in display_lines:
            self.image_buffer.put_at(1, y_offset, line, transparent=False)
            y_offset += 1

        is_active = self.active_process and self.active_process.poll() is None
        current_prompt = self.prompt if not is_active else ""
        self.image_buffer.put_at(
            1, y_offset, current_prompt + self.current_input + "_", transparent=False
        )

    def run(self, end_message=True):
        _win32 = sys.platform == "win32"
        _original_console_mode = None
        if _win32:
            import ctypes

            _ENABLE_PROCESSED_INPUT = 0x0001
            _stdin_handle = ctypes.windll.kernel32.GetStdHandle(-10)
            _mode = ctypes.c_ulong()
            ctypes.windll.kernel32.GetConsoleMode(_stdin_handle, ctypes.byref(_mode))
            _original_console_mode = _mode.value
            ctypes.windll.kernel32.SetConsoleMode(
                _stdin_handle, _original_console_mode & ~_ENABLE_PROCESSED_INPUT
            )

        try:
            self.clear_back_buffer()
            self.display_buffer.clear_buffer(val=self.background)

            frame = 0
            while self.frames == INF or frame < self.frames:
                frame_start = time.perf_counter()
                if self.screen.has_resized():
                    raise ScreenResizedError("Resized.")

                should_stop = False
                while True:
                    event = self.screen.get_event()
                    if event is None:
                        break

                    if event in (-1, 27, getattr(Screen, "KEY_ESCAPE", -1)):
                        should_stop = True
                        break
                    elif event in (10, 13):
                        self.execute_command()
                    elif event in (-300, 8, 127, getattr(Screen, "KEY_BACK", -300)):
                        self.current_input = self.current_input[:-1]
                    elif isinstance(event, int) and 32 <= event <= 126:
                        self.current_input += chr(event)

                if should_stop:
                    break

                self.render_to_back_buffer(frame)
                self.swap_buffers()
                self.present_frame()

                remaining = self.frame_time - (time.perf_counter() - frame_start)
                if remaining > 0:
                    sleep(remaining)
                frame += 1
        except KeyboardInterrupt:
            pass
        finally:
            if self.active_process:
                self.active_process.terminate()
            if _original_console_mode is not None:
                import ctypes

                ctypes.windll.kernel32.SetConsoleMode(
                    _stdin_handle, _original_console_mode
                )

        if end_message:
            self.render_exit_to_back_buffer()
            self.swap_buffers()
            self.present_frame()
            if _win32:
                try:
                    input()
                except KeyboardInterrupt:
                    pass
