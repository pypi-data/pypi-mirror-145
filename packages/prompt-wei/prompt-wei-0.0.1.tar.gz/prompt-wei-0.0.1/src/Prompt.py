from pynput import keyboard


class Prompt:
    _UP = 'A'
    _DOWN = 'B'
    _LEFT = ''
    _RIGHT = ''
    _HIDDEN = '?25l'
    _DISPLAY = '?25h'
    _PUSH = 's'
    _POP = 'u'
    _CHECK = '\u2713'

    def __init__(self, message, options, page=1) -> None:
        self.message = message
        self.options = options
        self.page = page
        self.cur = 0
        self.row = len(self.options) // self.page
        self.no = 1

    def _Cursor(self, op, step=0):
        if step:
            self._baseWrite('\33[{}{}'.format(step, op))
        else:
            self._baseWrite('\33[{}'.format(op))

    def _baseWrite(self, content):
        print(content, end='', flush=True)

    def _keyUp(self):
        if self.cur % self.row > 0:
            self._baseWrite('\b')
            self._baseWrite(' ')
            self._baseWrite('\b')
            self.cur -= 1
            self._Cursor(Prompt._UP, 1)
            self._baseWrite(Prompt._CHECK)

    def _keyDown(self):
        if self.cur % self.row < self.row - 1 and self.cur < len(self.options) - 1:
            self._baseWrite('\b')
            self._baseWrite(' ')
            self._baseWrite('\b')
            self.cur += 1
            self._Cursor(Prompt._DOWN, 1)
            self._baseWrite(Prompt._CHECK)

    def _display(self):
        print(self.message,':')
        for i in range((self.no - 1) * self.row, self.no * self.row):
            if i < len(self.options): print('  ', self.options[i])
            else : print()

    def selector(self):
        self._display()
        self._Cursor(Prompt._PUSH)
        self._Cursor(Prompt._UP,self.row)
        self._baseWrite(Prompt._CHECK)
        self._Cursor(Prompt._HIDDEN)

        def on_press(key):
            try:
                if key == keyboard.Key.up:
                    self._keyUp()
                if key == keyboard.Key.down:
                    self._keyDown()
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))

        def on_release(key):
            if key == keyboard.Key.enter:
                # Stop listener
                return False

        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release,
                suppress=True) as listener:
            listener.join()

        self._Cursor(Prompt._POP)
        self._Cursor(Prompt._DISPLAY)
        return self.options[self.cur]
