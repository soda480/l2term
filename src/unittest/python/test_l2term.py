import unittest
from mock import patch
from mock import call
from mock import Mock
from mock import MagicMock

from l2term import Lines
from l2term.l2term import MAX_LINES
from l2term.l2term import MAX_CHARS

import sys
import logging
logger = logging.getLogger(__name__)


class TestLines(unittest.TestCase):

    def setUp(self):
        """ setup
        """
        pass

    def tearDown(self):
        """ tear down
        """
        pass

    @patch('l2term.Lines._move_up')
    def test__get_move_char_Should_ReturnExpected_When_MovingUp(self, move_up_patch, *patches):
        term = Lines([''] * 13)
        term._current = 12
        result = term._get_move_char(7)
        self.assertEqual(result, move_up_patch.return_value)

    @patch('l2term.Lines._move_down')
    def test__get_move_char_Should_ReturnExpected_When_MovingDown(self, move_down_patch, *patches):
        term = Lines([''] * 13)
        term._current = 2
        result = term._get_move_char(7)
        self.assertEqual(result, move_down_patch.return_value)

    @patch('l2term.Lines._move_down')
    def test__get_move_char_Should_ReturnExpected_When_NotMoving(self, move_down_patch, *patches):
        term = Lines([''] * 13)
        term._current = 2
        result = term._get_move_char(2)
        self.assertEqual(result, '')

    @patch('l2term.l2term.Cursor.DOWN')
    def test__move_down_Should_CallExpected_When_Called(self, down_patch, *patches):
        term = Lines([''] * 13)
        term._current = 2
        result = term._move_down(7)
        self.assertEqual(result, down_patch.return_value)
        self.assertEqual(term._current, 7)

    @patch('l2term.l2term.Cursor.UP')
    def test__move_up_Should_ReturnExpected_When_Called(self, up_patch, *patches):
        term = Lines([''] * 13)
        term._current = 12
        result = term._move_up(7)
        self.assertEqual(result, up_patch.return_value)
        self.assertEqual(term._current, 7)

    @patch('l2term.Lines._validate')
    @patch('l2term.l2term.sys.stderr')
    @patch('l2term.l2term.cursor')
    def test__hide_cursor_Should_CallHideCursor_When_Tty(self, cursor_patch, stderr_patch, *patches):
        stderr_patch.isatty.return_value = True
        term = Lines([''] * 3)
        term.hide_cursor()
        cursor_patch.hide.assert_called_once_with()

    @patch('l2term.l2term.sys.stderr')
    @patch('l2term.l2term.cursor')
    def test__hide_cursor_Should_CallHideCursor_When_NoTty(self, cursor_patch, stderr_patch, *patches):
        stderr_patch.isatty.return_value = False
        term = Lines([''] * 3)
        term.hide_cursor()
        cursor_patch.hide.assert_not_called()

    @patch('l2term.Lines._validate')
    @patch('l2term.l2term.sys.stderr')
    @patch('l2term.l2term.cursor')
    def test__show_cursor_Should_CallShowCursor_When_Tty(self, cursor_patch, stderr_patch, *patches):
        stderr_patch.isatty.return_value = True
        term = Lines([''] * 3)
        term.show_cursor()
        cursor_patch.show.assert_called_once_with()

    @patch('l2term.l2term.sys.stderr')
    @patch('l2term.l2term.cursor')
    def test__show_cursor_Should_NotCallShowCursor_When_NoTty(self, cursor_patch, stderr_patch, *patches):
        stderr_patch.isatty.return_value = False
        term = Lines([''] * 3)
        term.show_cursor()
        cursor_patch.show.assert_not_called()

    @patch('l2term.Lines._validate')
    @patch('l2term.Lines.print_lines')
    @patch('l2term.Lines.hide_cursor')
    @patch('l2term.Lines.show_cursor')
    def test__enter_exit_Should_HideAndShowCursorAndPrintLines_When_Called(self, show_cursor_patch, hide_cursor_patch, print_lines_patch, *patches):
        with Lines([''] * 3):
            hide_cursor_patch.assert_called_once_with()
            print_lines_patch.assert_called_once_with(force=True)
        show_cursor_patch.assert_called_once_with()

    @patch('l2term.Lines.print_line')
    def test__set_item_Should_CallPrintLine_When_Called(self, print_line_patch, *patches):
        lines = Lines([''] * 3)
        lines[1] = 'hello world'
        print_line_patch.assert_called_once_with(1)

    @patch('l2term.Lines.print_lines')
    @patch('l2term.Lines._clear_line')
    def test__del_item_Should_CallClearLineAndPrintLines_When_Called(self, clear_line_patch, print_lines_patch, *patches):
        lines = Lines([''] * 3)
        del lines[1]
        clear_line_patch.assert_called_once_with(2)
        print_lines_patch.assert_called_once_with(1)

    @patch('l2term.Lines.print_lines')
    @patch('l2term.Lines._clear_line')
    def test__del_item_Should_RaiseNotImplementedError_When_CalledWithSlice(self, clear_line_patch, print_lines_patch, *patches):
        lines = Lines([''] * 3)
        with self.assertRaises(NotImplementedError):
            del lines[1:2]

    @patch('l2term.Lines.print_lines')
    def test_append_Should_CallPrintLines_When_Called(self, print_lines_patch, *patches):
        lines = Lines([''] * 3)
        lines.append('hello world')
        print_lines_patch.assert_called_once_with()

    @patch('l2term.Lines.print_lines')
    @patch('l2term.Lines._clear_line')
    def test_pop_Should_CallClearLineAndPrintLines_When_Called(self, clear_line_patch, print_lines_patch, *patches):
        lines = Lines([''] * 3)
        lines.pop(1)
        clear_line_patch.assert_called_once_with(2)
        print_lines_patch.assert_called_once_with(1)

    def test__remove_Should_RaiseNotImplementedError_When_Called(self, *patches):
        lines = Lines([''] * 3)
        with self.assertRaises(NotImplementedError):
            lines.remove('hello world')

    @patch('l2term.Lines._clear_line')
    def test_clear_Should_CallClearLineForAllLines_When_Called(self, clear_line_patch, *patches):
        lines = Lines([''] * 3)
        lines.clear()
        for number in range(3):
            self.assertTrue(call(number) in clear_line_patch.mock_calls)

    @patch('l2term.Lines._validate')
    @patch('l2term.l2term.sys.stderr.isatty', return_value=True)
    @patch('l2term.Lines._get_move_char')
    @patch('builtins.print')
    def test__clear_line_Should_CallExpected_When_Tty(self, print_patch, get_move_char_patch, *patches):
        lines = Lines([''] * 3)
        lines._clear_line(1)
        get_move_char_patch.assert_called_once_with(1)
        print_patch.assert_called()

    @patch('l2term.Lines._validate')
    @patch('l2term.Lines._get_move_char')
    @patch('l2term.l2term.sys.stderr')
    @patch('builtins.print')
    def test__print_line_Should_CallExpected_When_Tty(self, print_patch, stderr_patch, *patches):
        stderr_patch.isatty.return_value = True
        term = Lines([''] * 13)
        term._current = 0
        term.print_line(3)
        self.assertEqual(len(print_patch.mock_calls), 2)
        self.assertEqual(term._current, 1)

    @patch('l2term.l2term.sys.stderr')
    @patch('builtins.print')
    def test__print_line_Should_CallExpected_When_Notty(self, print_patch, stderr_patch, *patches):
        stderr_patch.isatty.return_value = False
        term = Lines([''] * 13)
        term._current = 0
        term.print_line(3)
        print_patch.assert_not_called()
        self.assertEqual(term._current, 0)

    @patch('l2term.Lines._get_move_char')
    @patch('l2term.l2term.sys.stderr')
    @patch('builtins.print')
    def test__print_line_Should_CallExpected_When_NoTtyButForce(self, print_patch, stderr_patch, *patches):
        stderr_patch.isatty.return_value = False
        term = Lines([''] * 13)
        term._current = 0
        term.print_line(3, force=True)
        self.assertEqual(len(print_patch.mock_calls), 2)
        self.assertEqual(term._current, 1)

    @patch('l2term.Lines.print_line')
    def test__print_lines_Should_CallExpected_When_Called(self, print_line_patch, *patches):
        term = Lines([''] * 3)
        term.print_lines()
        self.assertEqual(len(print_line_patch.mock_calls), 3)

    @patch('l2term.l2term.sys.stderr.isatty', return_value=True)
    @patch('l2term.l2term.os.get_terminal_size')
    def test__validate_Should_RaiseValueError_When_TtyTerminalLinesLessThanListSize(self, get_terminal_size_patch, *patches):
        get_terminal_size_patch.return_value = Mock(lines=2)
        with self.assertRaises(ValueError):
            Lines([''] * 3)

    @patch('l2term.l2term.sys.stderr.isatty', return_value=False)
    def test__validate_Should_RaiseValueError_When_NoTtyListSizeGreaterThanMaxAllowed(self, *patches):
        with self.assertRaises(ValueError):
            Lines([''] * 300)

    def test__sanitize_Should_ReturnExpected_When_StrLessThanMaxChars(self, *patches):
        term = Lines([''] * 3)
        text = 'hello world'
        result = term._sanitize(text)
        self.assertEqual(result, text)

    def test__sanitize_Should_ReturnExpected_When_StrGreaterThanMaxChars(self, *patches):
        term = Lines([''] * 3)
        text = 'hello' * 40
        result = term._sanitize(text)
        expected_result = f'{text[0:MAX_CHARS - 3]}...'
        self.assertEqual(result, expected_result)

    def test__sanitize_Should_ReturnExpected_When_NoData(self, *patches):
        term = Lines([''] * 3)
        text = ''
        result = term._sanitize(text)
        self.assertEqual(result, text)

    def test__sanitize_Should_ReturnExpected_When_List(self, *patches):
        term = Lines([''] * 3)
        text = ['', 'i', ' ', 'a', 'm']
        result = term._sanitize(text)
        self.assertEqual(result, 'i am')
