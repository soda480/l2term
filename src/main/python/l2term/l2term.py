import os
import sys
import logging
from collections import UserList
from colorama import init as colorama_init
from colorama import Style
from colorama import Fore
from colorama import Back
from colorama import Cursor
import cursor

logger = logging.getLogger(__name__)

MAX_LINES = 75
MAX_CHARS = 120
CLEAR_EOL = '\033[K'


class Lines(UserList):

    def __init__(self, *args, show_index=True):
        """ constructor
        """
        logger.debug('executing Lines constructor')
        super().__init__(*args)
        self._max_chars = MAX_CHARS
        self._fill = len(str(len(self.data)))
        self._validate()
        self._current = 0
        self._show_index = show_index
        colorama_init()

    def __enter__(self):
        """ on entry hide cursor if stderr is attached to tty
        """
        self.hide_cursor()
        self.print_lines(force=True)
        return self

    def __exit__(self, *args):
        """ on exit show cursor if stderr is attached to tty and print items
        """
        self.print_lines(force=True)
        self.show_cursor()

    def __setitem__(self, index, item):
        """ set item override
        """
        super().__setitem__(index, item)
        self.print_line(index)

    def __delitem__(self, index):
        """ delete item override
        """
        original_len = len(self.data)
        super().__delitem__(index)
        if isinstance(index, int):
            # clear last line
            self._clear_line(original_len - 1)
            start = index if index > 0 else None
            self.print_lines(start)
        else:
            # for number in range(index.stop, original_len):
            #    self._clear_line(number)
            # self.print_lines(index.start)
            raise NotImplementedError('deleting slices is not supported')

    def append(self, item):
        """ append override
        """
        # need to add some validation here
        super().append(item)
        self.print_lines()

    def pop(self, index=-1):
        """ pop override
        """
        super().pop(index)
        # clear supposed last line in terminal
        self._clear_line(len(self.data))
        start = index if index > 0 else None
        self.print_lines(start)

    def remove(self, item):
        """ remove override
        """
        raise NotImplementedError('remove is not supported')

    def clear(self):
        """ clear override
        """
        original_len = len(self.data)
        self.data.clear()
        for number in range(0, original_len):
            self._clear_line(number)

    def _clear_line(self, index):
        """ clear line at index
        """
        if sys.stderr.isatty():
            move_char = self._get_move_char(index)
            print(f'{move_char}{CLEAR_EOL}', end='', file=sys.stderr)

    def print_line(self, index, force=False):
        """ move to index and print item at index
        """
        if sys.stderr.isatty() or force:
            str_index = ''
            if self._show_index:
                bright_yellow = Style.BRIGHT + Fore.YELLOW + Back.BLACK
                str_index = f"{bright_yellow}{str(index).zfill(self._fill)}{Style.RESET_ALL}: "

            move_char = self._get_move_char(index)
            print(f'{move_char}{CLEAR_EOL}', end='', file=sys.stderr)
            sanitized = self._sanitize(self.data[index])
            print(f'{str_index}{sanitized}', file=sys.stderr)
            sys.stderr.flush()
            self._current += 1

    def print_lines(self, force=False, from_index=None):
        """ print all items
        """
        if from_index is None:
            from_index = 0
        logger.info(f'printing all items starting at index {from_index}')
        for index, _ in enumerate(self.data[from_index:], from_index):
            self.print_line(index, force=force)

    def _get_move_char(self, index):
        """ return char to move to index
        """
        move_char = ''
        if index < self._current:
            move_char = self._move_up(index)
        elif index > self._current:
            move_char = self._move_down(index)
        return move_char

    def _move_down(self, index):
        """ return char to move down to index and update current
        """
        diff = index - self._current
        self._current += diff
        return Cursor.DOWN(diff)

    def _move_up(self, index):
        """ return char to move up to index and update current
        """
        diff = self._current - index
        self._current -= diff
        return Cursor.UP(diff)

    def show_cursor(self):
        """ show cursor
        """
        if sys.stderr.isatty():
            cursor.show()

    def hide_cursor(self):
        """ hide cursor
        """
        if sys.stderr.isatty():
            cursor.hide()

    def _validate(self):
        """ validate and set max chars if tty
        """
        if sys.stderr.isatty():
            size = os.get_terminal_size()
            if len(self.data) > size.lines:
                raise ValueError(f'number of items to display exceeds current terminal size {size.lines}')
            # self._max_chars = size.columns
        else:
            if len(self.data) > MAX_LINES:
                raise ValueError(f'number of items to display exceeds allowed size {MAX_LINES}')

    def _sanitize(self, item):
        """ sanitize item
        """
        if item:
            if isinstance(item, str):
                item = item.splitlines()[0]
                if len(item) > self._max_chars:
                    item = f'{item[0:self._max_chars - 3]}...'
            else:
                item = ''.join(i for i in item)
        return item
