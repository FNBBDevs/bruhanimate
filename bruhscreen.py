"""
Much of bruhscreen implementation is based on the Windows based implementation of 
setting of terminal screen from AsciiMatics found here at <https://github.com/peterbrittain/asciimatics>
and more specifically at <https://github.com/peterbrittain/asciimatics/blob/master/asciimatics/screen.py>
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import sys
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_QUICK_EDIT_MODE = 0x0040

if sys.platform == 'win32':
    import win32con
    

    import win32console
    import win32event
    import win32file
    import pywintypes

    class WinScreen:
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
                self._stdout.WriteConsole(text)
                self._current_x = x + width
                self._current_y = y
            except pywintypes.error:
                pass
        
        def print_center(self, text, y, width):
            try:
                left_pad = (self.width - width) // 2
                self._stdout.SetConsoleCursorPosition(win32console.PyCOORDType(left_pad, y))
                self._stdout.WriteConsole(text)
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


            screen = WinScreen(win_out, win_in, old_out, in_mode)
            return screen
            
        @classmethod
        def show(cls, function, args=None):
            screen = WinScreen.open()
            try:
                if args:
                    return function(screen, *args)
                else:
                    return function(screen)
            finally:
                screen.close()


