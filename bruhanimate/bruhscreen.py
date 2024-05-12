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
        # Standard extended key codes.
        KEY_ESCAPE = -1
        KEY_F1 = -2
        KEY_F2 = -3
        KEY_F3 = -4
        KEY_F4 = -5
        KEY_F5 = -6
        KEY_F6 = -7
        KEY_F7 = -8
        KEY_F8 = -9
        KEY_F9 = -10
        KEY_F10 = -11
        KEY_F11 = -12
        KEY_F12 = -13
        KEY_F13 = -14
        KEY_F14 = -15
        KEY_F15 = -16
        KEY_F16 = -17
        KEY_F17 = -18
        KEY_F18 = -19
        KEY_F19 = -20
        KEY_F20 = -21
        KEY_F21 = -22
        KEY_F22 = -23
        KEY_F23 = -24
        KEY_F24 = -25
        KEY_PRINT_SCREEN = -100
        KEY_INSERT = -101
        KEY_DELETE = -102
        KEY_HOME = -200
        KEY_END = -201
        KEY_LEFT = -203
        KEY_UP = -204
        KEY_RIGHT = -205
        KEY_DOWN = -206
        KEY_PAGE_UP = -207
        KEY_PAGE_DOWN = -208
        KEY_BACK = -300
        KEY_TAB = -301
        KEY_BACK_TAB = -302
        KEY_NUMPAD0 = -400
        KEY_NUMPAD1 = -401
        KEY_NUMPAD2 = -402
        KEY_NUMPAD3 = -403
        KEY_NUMPAD4 = -404
        KEY_NUMPAD5 = -405
        KEY_NUMPAD6 = -406
        KEY_NUMPAD7 = -407
        KEY_NUMPAD8 = -408
        KEY_NUMPAD9 = -409
        KEY_MULTIPLY = -410
        KEY_ADD = -411
        KEY_SUBTRACT = -412
        KEY_DECIMAL = -413
        KEY_DIVIDE = -414
        KEY_CAPS_LOCK = -500
        KEY_NUM_LOCK = -501
        KEY_SCROLL_LOCK = -502
        KEY_SHIFT = -600
        KEY_CONTROL = -601
        KEY_MENU = -602

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
            self._KEY_MAP = {
                win32con.VK_ESCAPE: Screen.KEY_ESCAPE,
                win32con.VK_F1: Screen.KEY_F1,
                win32con.VK_F2: Screen.KEY_F2,
                win32con.VK_F3: Screen.KEY_F3,
                win32con.VK_F4: Screen.KEY_F4,
                win32con.VK_F5: Screen.KEY_F5,
                win32con.VK_F6: Screen.KEY_F6,
                win32con.VK_F7: Screen.KEY_F7,
                win32con.VK_F8: Screen.KEY_F8,
                win32con.VK_F9: Screen.KEY_F9,
                win32con.VK_F10: Screen.KEY_F10,
                win32con.VK_F11: Screen.KEY_F11,
                win32con.VK_F12: Screen.KEY_F12,
                win32con.VK_F13: Screen.KEY_F13,
                win32con.VK_F14: Screen.KEY_F14,
                win32con.VK_F15: Screen.KEY_F15,
                win32con.VK_F16: Screen.KEY_F16,
                win32con.VK_F17: Screen.KEY_F17,
                win32con.VK_F18: Screen.KEY_F18,
                win32con.VK_F19: Screen.KEY_F19,
                win32con.VK_F20: Screen.KEY_F20,
                win32con.VK_F21: Screen.KEY_F21,
                win32con.VK_F22: Screen.KEY_F22,
                win32con.VK_F23: Screen.KEY_F23,
                win32con.VK_F24: Screen.KEY_F24,
                win32con.VK_PRINT: Screen.KEY_PRINT_SCREEN,
                win32con.VK_INSERT: Screen.KEY_INSERT,
                win32con.VK_DELETE: Screen.KEY_DELETE,
                win32con.VK_HOME: Screen.KEY_HOME,
                win32con.VK_END: Screen.KEY_END,
                win32con.VK_LEFT: Screen.KEY_LEFT,
                win32con.VK_UP: Screen.KEY_UP,
                win32con.VK_RIGHT: Screen.KEY_RIGHT,
                win32con.VK_DOWN: Screen.KEY_DOWN,
                win32con.VK_PRIOR: Screen.KEY_PAGE_UP,
                win32con.VK_NEXT: Screen.KEY_PAGE_DOWN,
                win32con.VK_BACK: Screen.KEY_BACK,
                win32con.VK_TAB: Screen.KEY_TAB
            }
            self._keys = set()
            self._map_all = False

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
        
        def has_resized(self):
            re_sized = False
            info = self._stdout.GetConsoleScreenBufferInfo()['Window']
            width = info.Right - info.Left + 1
            height = info.Bottom - info.Top + 1
            if width != self._last_width or height != self._last_height:
                re_sized = True
            return re_sized

        def set_title(self, title):
            win32console.SetConsoleTitle(title)
        
        def wait_for_input(self, timeout):
            rc = win32event.WaitForSingleObject(self._stdin, int(timeout * 1000))
            if rc not in [0, 258]:
                raise RuntimeError(rc)

        def get_event(self):
            """
            Check for any event without waiting.
            """
            # Look for a new event and consume it if there is one.
            while len(self._stdin.PeekConsoleInput(1)) > 0:
                event = self._stdin.ReadConsoleInput(1)[0]
                if event.EventType == win32console.KEY_EVENT:
                    # Pasting unicode text appears to just generate key-up
                    # events (as if you had pressed the Alt keys plus the
                    # keypad code for the character), but the rest of the
                    # console input simply doesn't
                    # work with key up events - e.g. misses keyboard repeats.
                    #
                    # We therefore allow any key press (i.e. KeyDown) event and
                    # _any_ event that appears to have popped up from nowhere
                    # as long as the Alt key is present.
                    key_code = ord(event.Char)
                    if (event.KeyDown or
                            (key_code > 0 and key_code not in self._keys and
                             event.VirtualKeyCode == win32con.VK_MENU)):
                        # Record any keys that were pressed.
                        if event.KeyDown:
                            self._keys.add(key_code)

                        # Translate keys into a KeyboardEvent object.
                        if event.VirtualKeyCode in self._KEY_MAP:
                            key_code = self._KEY_MAP[event.VirtualKeyCode]

                        # Sadly, we are limited to Linux terminal input and so
                        # can't return modifier states in a cross-platform way.
                        # If the user decided not to be cross-platform, so be
                        # it, otherwise map some standard bindings for extended
                        # keys.
                        if (self._map_all and
                                event.VirtualKeyCode in self._EXTRA_KEY_MAP):
                            key_code = self._EXTRA_KEY_MAP[event.VirtualKeyCode]
                        elif (event.VirtualKeyCode == win32con.VK_TAB and
                                    event.ControlKeyState &
                                    win32con.SHIFT_PRESSED):
                                key_code = Screen.KEY_BACK_TAB
                        elif (event.VirtualKeyCode == win32con.VK_RETURN):
                            key_code = 10
                        elif (event.VirtualKeyCode == win32con.VK_TAB):
                            key_code = 11
     

                        # Don't return anything if we didn't have a valid
                        # mapping.
                        if key_code:
                            return key_code
                    else:
                        # Tidy up any key that was previously pressed.  At
                        # start-up, we may be mid-key, so can't assume this must
                        # always match up.
                        if key_code in self._keys:
                            self._keys.remove(key_code)

            # If we get here, we've fully processed the event queue and found
            # nothing interesting.
            return None


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

        def has_resized(self):
            return self._re_sized

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
