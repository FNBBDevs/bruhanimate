"""
Copyright 2023 Ethan Christensen
Copied, Guided, and Adapted from Asciimatics <https://github.com/peterbrittain/asciimatics/blob/master/asciimatics/screen.py>

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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import signal

import sys
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_QUICK_EDIT_MODE = 0x0040

if sys.platform == 'win32':
    import win32con
    import win32event # -->. for keyboard events

    import win32console
    import win32file
    import pywintypes

    class Screen:
        """
        Class for creating and managing a terminal screen in a WINDOWS OS terminal
        """
        def __init__(self, stdout, stdin, old_out, old_in):
            info = stdout.GetConsoleScreenBufferInfo()['Window']
            self.width = info.Right - info.Left + 1
            self.height = info.Bottom - info.Top + 1
            self._stdout = stdout
            self._stdin = stdin
            self._last_width = self.width
            self._last_height = self.height
            self._last_start = 0
            self._old_out = old_out
            self._old_in = old_in
            self._current_x = 0
            self._current_y = 0

        def close(self, restore=True):
            if restore:
                self._old_out.SetConsoleActiveScreenBuffer()
                self._stdin.SetConsoleMode(self._old_in)

        def print_at(self, text, x, y, width):
            try:
                if x != self._current_x or y != self._current_y:
                    self._stdout.SetConsoleCursorPosition(win32console.PyCOORDType(x, y))
                self._stdout.WriteConsole(str(text))
                self._current_x = x + width
                self._current_y = y
            except pywintypes.error:
                pass
        
        def print_center(self, text, y, width):
            try:
                left_pad = (self.width - width) // 2
                self._stdout.SetConsoleCursorPosition(win32console.PyCOORDType(left_pad, y))
                self._stdout.WriteConsole(str(text))
                self._current_x = left_pad + width
                self._current_y = y
            except pywintypes.error:
                pass
        
        def clear(self):
            info = self._stdout.GetConsoleScreenBufferInfo()['Window']
            width = info.Right - info.Left + 1
            height = info.Bottom - info.Top + 1
            box_size = width * height
            self._stdout.FillConsoleOutputAttribute(
                0, box_size, win32console.PyCOORDType(0, 0))
            self._stdout.FillConsoleOutputCharacter(
                " ", box_size, win32console.PyCOORDType(0, 0))
            self._stdout.SetConsoleCursorPosition(
                win32console.PyCOORDType(0, 0))
        
        @classmethod
        def open(cls):
            old_out = win32console.PyConsoleScreenBufferType(win32file.CreateFile("CONOUT$", win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                                                                                    win32file.FILE_SHARE_WRITE, None, win32file.OPEN_ALWAYS, 0, None))
            try:
                info = old_out.GetConsoleScreenBufferInfo()
            except pywintypes.error:
                info = None
            win_out = win32console.CreateConsoleScreenBuffer()
            if info:
                win_out.SetConsoleScreenBufferSize(info['Size'])
            else:
                win_out.SetStdHandle(win32console.STD_OUTPUT_HANDLE)
            win_out.SetConsoleActiveScreenBuffer()
            win_in = win32console.PyConsoleScreenBufferType(
                win32file.CreateFile("CONIN$",
                                        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                                        win32file.FILE_SHARE_READ,
                                        None,
                                        win32file.OPEN_ALWAYS,
                                        0,
                                        None))
            win_in.SetStdHandle(win32console.STD_INPUT_HANDLE)
            # Hide Cursor
            win_out.SetConsoleCursorInfo(1, 0)
            # Disable scroll
            out_mode = win_out.GetConsoleMode()
            win_out.SetConsoleMode(
                out_mode & ~ win32console.ENABLE_WRAP_AT_EOL_OUTPUT)
            in_mode = win_in.GetConsoleMode()
            new_mode = (in_mode | win32console.ENABLE_MOUSE_INPUT |
                            ENABLE_EXTENDED_FLAGS)
            new_mode &= ~ENABLE_QUICK_EDIT_MODE
            #new_mode &= ~win32console.ENABLE_PROCESSED_INPUT
            win_in.SetConsoleMode(new_mode)


            screen = Screen(win_out, win_in, old_out, in_mode)
            return screen
            
        @classmethod
        def show(cls, function, args=None):
            screen = Screen.open()
            try:
                if args:
                    return function(screen, *args)
                else:
                    return function(screen)
            finally:
                screen.close()

else:
    import curses
    import termios
    import select

    class Screen:
        def __init__(self, window, height=None):
            self.screen = window
            self.screen.keypad(1)
            self.height = window.getmaxyx()[0]
            self.width  = window.getmaxyx()[1]
            curses.curs_set(0)
            self.screen.nodelay(1)
            self.signal_state = SignalState()
            self._re_sized = False
            self.signal_state.set(signal.SIGWINCH, self._resize_handler)
            self.signal_state.set(signal.SIGCONT, self._continue_handler)
            curses.mousemask(curses.ALL_MOUSE_EVENTS |
                                curses.REPORT_MOUSE_POSITION)
            self._move_y_x = curses.tigetstr("cup")
            self._up_line = curses.tigetstr("ri").decode("utf-8")
            self._down_line = curses.tigetstr("ind").decode("utf-8")
            self._fg_color = curses.tigetstr("setaf")
            self._bg_color = curses.tigetstr("setab")
            self._default_colours = curses.tigetstr("op")
            if curses.tigetflag("hs"):
                self._start_title = curses.tigetstr("tsl").decode("utf-8")
                self._end_title = curses.tigetstr("fsl").decode("utf-8")
            else:
                self._start_title = self._end_title = None
            self._a_normal = curses.tigetstr("sgr0").decode("utf-8")
            self._a_bold = curses.tigetstr("bold").decode("utf-8")
            self._a_reverse = curses.tigetstr("rev").decode("utf-8")
            self._a_underline = curses.tigetstr("smul").decode("utf-8")
            self._clear_screen = curses.tigetstr("clear").decode("utf-8")
            self._bytes_to_read = 0
            self._bytes_to_return = b""
            self._cur_x = 0
            self._cur_y = 0
        
        def _resize_handler(self, *_):
            curses.endwin()
            curses.initscr()
            self._re_sized = True
        
        def _continue_handler(self, *_):
            self.force_update(full_refresh=True)

        def close(self, restore=True):
            self.signal_state.restore()
            if restore:
                self.screen.keypad(0)
                curses.echo()
                curses.nocbreak()
                curses.endwin()
        
        def clear(self):
            try:
                sys.stdout.flush()
                os.system("clear")
            except IOError:
                pass

        @classmethod
        def open(cls):
            stdcrs = curses.initscr()
            curses.noecho()
            curses.cbreak()
            stdcrs.keypad(1)
            screen = Screen(stdcrs)
            return screen

        @staticmethod
        def _safe_write(msg):
            try:
                sys.stdout.write(msg)
            except IOError:
                pass
        
        def print_at(self, text, x, y, width):
            cursor = u""
            if x != self._cur_x or y != self._cur_y:
                cursor = curses.tparm(self._move_y_x, y, x).decode("utf-8")
            try:
                self._safe_write(cursor + str(text))
            except UnicodeEncodeError:
                self._safe_write(cursor + "?" * len(text))

            self._cur_x = x + width
            self._cur_y = y
        
        @classmethod
        def show(cls, function, args=None):
            os.system("clear")
            screen = Screen.open()
            try:
                if args:
                    return function(screen, *args)
                else:
                    return function(screen)
            finally:
                screen.close()
                input()
                os.system("clear")
                

    class SignalState(object):
            def __init__(self):
                self._old_signal_states = []

            def set(self, signalnum, handler):
                old_handler = signal.getsignal(signalnum)
                if old_handler is None:
                    old_handler = signal.SIG_DFL
                self._old_signal_states.append((signalnum, old_handler))
                signal.signal(signalnum, handler)

            def restore(self):
                for signalnum, handler in self._old_signal_states:
                    signal.signal(signalnum, handler)
                self._old_signal_states = []
