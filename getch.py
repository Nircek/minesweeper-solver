#!/usr/bin/env python3
# inspired by http://code.activestate.com/recipes/134892/
try:
    import msvcrt
    getch = msvcrt.getch
except ImportError:
    import sys
    import tty
    import termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
