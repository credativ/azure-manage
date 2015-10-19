# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import fcntl
import termios
import struct
import sys


class ProgressMeter:
    def __init__(self, stream, total, count=0):
        self.stream = stream
        self.total = total
        self.count = count

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.clear()

    def clear(self):
        self.stream.write_progress('')

    def display(self):
        self.stream.write_progress('%d/%d %d%%' % (self.count, self.total, self.count / self.total * 100))

    def set(self, count):
        self.count = min(count, self.total)
        self.display()

    def update(self, count):
        self.set(self.count + count)


class ProgressOutput:
    def __init__(self):
        self.stream = sys.stdout
        self._terminal_nr_rows = None

    def __enter__(self):
        self._terminal_size = self._TIOCGWINSZ(1)

        if self._terminal_size:
            self._setup_terminal(self._terminal_size[0])

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._terminal_size:
            self._setup_terminal(self._terminal_size[0] + 1)
        self._terminal_nr_rows = None

    def _setup_terminal(self, nr_rows):
        self.stream.write("\n")
        # save cursor
        self.stream.write("\033[s")

        # set scroll region (this will place the cursor in the top left)
        self.stream.write("\033[0;{}r".format(nr_rows - 1))

        # restore cursor but ensure its inside the scrolling area
        self.stream.write("\033[u\033[1A")

        self.stream.flush()

    def _TIOCGWINSZ(self, fd):
        try:
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr

    def write_progress(self, s):
        if not self._terminal_size:
            return

        # save cursor
        self.stream.write("\033[s")
        # move cursor position to last row
        self.stream.write("\033[{};0f".format(self._terminal_size[0]))
        # set color
        self.stream.write("\033[30m\033[42m")
        # clear line
        self.stream.write("\033[K")
        try:
            self.stream.write('Progress: ')
            self.stream.write(str(s))
        finally:
            # reset color
            self.stream.write("\033[39m\033[49m")
            # reset cursor
            self.stream.write("\033[u")
            self.stream.flush()
