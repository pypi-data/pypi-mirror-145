import os
import sys
from enum import Enum


class Key(Enum):
    """ keyboard keys """
    ENTER = [10]
    ESC = [27]
    ARROW_UP = [27, 91, 65]
    ARROW_DOWN = [27, 91, 66]
    ARROW_LEFT = [27, 91, 68]
    ARROW_RIGHT = [27, 91, 67]
    PAGE_UP = [27, 91, 53, 126]
    PAGE_DOWN = [27, 91, 54, 126]
    HOME = [27, 91, 72]
    END = [27, 91, 70]
    BACKSPACE = [127]
    INSERT = [27, 91, 50, 126]
    DELETE = [27, 91, 51, 126]

    ARROWS = [ARROW_UP, ARROW_DOWN, ARROW_LEFT, ARROW_RIGHT]

    def __repr__(self):  # pragma: no cover
        return self.name + str(self.code)

    @property
    def code(self):  # pragma: no cover
        """
        Key code
        :rtype: list[int]
        """
        return self.value if self != Key.ARROWS else []

    @staticmethod
    def get_key(code):
        """
        Returns the Key with the code argument
        :param list[str] code: O Código
        :rtype: Key
        """
        for t in Key:
            if t != Key.ARROWS and code == [chr(_c) for _c in t.code]:
                return t


class _Getch(object):  # pragma: no cover
    """ Gets a single character from standard input.  Does not _echo to the screen. """

    class _GetchTimeOutException(Exception):
        pass

    def __init__(self):
        import sys
        if not os.isatty(sys.stdin.fileno()):
            self.impl = _Getch.debug_mode
        else:
            try:
                # noinspection PyUnresolvedReferences
                import msvcrt
                self.impl = msvcrt.getch()

            except ImportError:
                def _getch():
                    import tty
                    import termios
                    old_settings = termios.tcgetattr(sys.stdin)
                    try:
                        tty.setcbreak(sys.stdin.fileno())
                        ch = sys.stdin.read(1)
                    finally:
                        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    return ch[0]

                self.impl = _getch

    def __call__(self, block=True, translate_commands=False, echo=False):
        if not block:
            if not os.isatty(sys.stdin.fileno()):
                return -1
                # return _Getch.modo_debug()
            else:
                import signal
                signal.signal(signal.SIGALRM, _Getch.alarm_handler)
                signal.setitimer(signal.ITIMER_REAL, 0.01)
                try:
                    resp = self.impl()
                    signal.alarm(0)
                except _Getch._GetchTimeOutException:
                    signal.signal(signal.SIGALRM, signal.SIG_IGN)
                    resp = -1
        elif translate_commands:
            commands = []
            resp = self.impl()
            while resp != -1:
                commands.append(resp)
                resp = self(False)
            key = Key.get_key(commands)
            if key:
                resp = key
            elif len(commands) == 1:
                resp = commands[0]
            elif commands:
                resp = commands
        else:
            resp = self.impl()

        if echo:
            if resp not in Key:
                print(resp, end='', flush=True)
        return resp

    @staticmethod
    def debug_mode() -> str:
        """ Uses input instead getch and simulates keys """
        code = []  # type list[str]
        input_text = input().strip(' ')
        if input_text:
            if len(input_text) > 1 and input_text.startswith('n') and (
                    input_text[1:].isdigit() or input_text[1] == '-' and input_text[2:].isdigit()):
                code = [chr(int(input_text[1:]))]
            elif input_text.startswith('t'):
                if input_text in ['tAD']:  # Shortcuts
                    code = [chr(_c) for _c in Key.ARROW_DOWN.code]
                else:
                    for t in Key:
                        if t.nome == input_text[1:]:
                            code = [chr(_c) for _c in t.code]
                            break
            else:
                code = [input_text]
        else:
            code = ['']

        return code[0]

    @staticmethod
    def alarm_handler(signum, frame):
        raise _Getch._GetchTimeOutException


def getch(block: bool = True, translate_commands: bool = False):  # pragma: no cover
    """
    Returns a char ou Key typed by the user.

    :param translate_commands: Returns the Key instead of the command code
    :rtype: str | _Key
    """
    # noinspection PyProtectedMember
    return _Getch()(block=block, translate_commands=translate_commands)


def getche(block: bool = True, translate_commands=False):  # pragma: no cover
    """
    Returns a char ou Key typed by the user and print in terminal.

    :param translate_commands: Returns the Key instead of the command code
    :rtype: str | _Key
    """
    # noinspection PyProtectedMember
    return _Getch()(block=block, translate_commands=translate_commands, echo=True)
