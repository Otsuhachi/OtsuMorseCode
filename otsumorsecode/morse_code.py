import time

from typing import cast
from winsound import Beep

from otsuvalidator import VInt, VRegex, VString

C2M_TABLE = {
    '.': (0, 1, 0, 1, 0, 1),
    ',': (1, 1, 0, 0, 1, 1),
    '?': (0, 0, 1, 1, 0, 0),
    '_': (0, 0, 1, 1, 0, 1),
    '+': (0, 1, 0, 1, 0),
    '-': (1, 0, 0, 0, 0, 1),
    '×': (1, 0, 0, 1),
    '^': (0, 0, 0, 0, 0, 0),
    '/': (1, 0, 0, 1, 0),
    '@': (0, 1, 1, 0, 1, 0),
    '(': (1, 0, 1, 1, 0),
    ')': (1, 0, 1, 1, 0, 1),
    '"': (0, 1, 0, 0, 1, 0),
    '\'': (0, 1, 1, 1, 1, 0),
    '=': (1, 0, 0, 0, 1),
    'A': (0, 1),
    'B': (1, 0, 0, 0),
    'C': (1, 0, 1, 0),
    'D': (1, 0, 0),
    'E': (0, ),
    'F': (0, 0, 1, 0),
    'G': (1, 1, 0),
    'H': (0, 0, 0, 0),
    'I': (0, 0),
    'J': (0, 1, 1, 1),
    'K': (1, 0, 1),
    'L': (0, 1, 0, 0),
    'M': (1, 1),
    'N': (1, 0),
    'O': (1, 1, 1),
    'P': (0, 1, 1, 0),
    'Q': (1, 1, 0, 1),
    'R': (0, 1, 0),
    'S': (0, 0, 0),
    'T': (1, ),
    'U': (0, 0, 1),
    'V': (0, 0, 0, 1),
    'W': (0, 1, 1),
    'X': (1, 0, 0, 1),
    'Y': (1, 0, 1, 1),
    'Z': (1, 1, 0, 0),
    '1': (0, 1, 1, 1, 1),
    '2': (0, 0, 1, 1, 1),
    '3': (0, 0, 0, 1, 1),
    '4': (0, 0, 0, 0, 1),
    '5': (0, 0, 0, 0, 0),
    '6': (1, 0, 0, 0, 0),
    '7': (1, 1, 0, 0, 0),
    '8': (1, 1, 1, 0, 0),
    '9': (1, 1, 1, 1, 0),
    '0': (1, 1, 1, 1, 1),
}

M2C_TABLE = {x[1]: x[0] for x in C2M_TABLE.items()}

MORSE_CODE_REGEX = '^[A-Z0-9 \\.,\\?_\\+\\-×\\^\\/@\\(\\)"\'=]*$'


class MorseCode:
    """モールス信号クラスです。

    文字列のモールス表現を取得したり、モールス信号音を再生することができます。
    """

    text: str = cast(str, VRegex(MORSE_CODE_REGEX, 1))
    short: str = cast(str, VString(1, 1))
    long: str = cast(str, VString(1, 1))
    sep: str = cast(str, VString(1, 1))
    frequency: int = cast(int, VInt(37, 32767))
    minimum_length: int = cast(int, VInt(1))

    def __init__(self, text: str, *, short: str = '.', long: str = '-', sep: str = ' ', frequency: int = 440, minimum_length: int = 100):
        """textを表現するモールス信号を生成します。

        textに含むことができる文字は"A-Z0-9 .,?-@"です。
        また、連続する空白は1つとして扱われます。

        Args:
            text (str): 元となる文字列です。
            short (str, optional): 短点に使用する文字です。
            long (str, optional): 長点に使用する文字です。
            sep (str, optional): 文字間の区切りに使用する文字です。
            frequency (int, optional): 再生時の周波数Hzです。
            minimum_length (int, optional): 再生時の短点の長さです。

        Raises:
            ValueError: short, long, sepに重複する文字をあてることはできません。
        """
        if len({short, long, sep}) != 3:
            msg = 'short, long, sepはそれぞれ違う文字である必要があります。'
            raise ValueError(msg)
        self.short = short
        self.long = long
        self.sep = sep
        self.frequency = frequency
        self.minimum_length = minimum_length
        while '  ' in text:
            text = text.replace('  ', ' ')
        self.text = text.upper()
        ct = C2M_TABLE
        s = self.short
        l = self.long
        res = []
        for c in self.text:
            if c == ' ':
                res.append(' ')
            else:
                res.append(''.join(map(lambda x: l if x else s, ct[c])))
        self.__morse_code = self.sep.join(res)

    def __str__(self) -> str:
        return self.text

    def __add__(self, other) -> 'MorseCode':
        kwargs = {
            'short': self.short,
            'long': self.long,
            'sep': self.sep,
            'minimum_length': self.minimum_length,
        }

        if type(other) is MorseCode or type(getattr(other, 'text', None)) is str:
            kwargs['text'] = self.text + other.text
        else:
            kwargs['text'] = self.text + other
        return MorseCode(**kwargs)

    @property
    def morse_code(self) -> str:
        """モールス表現化した文字列を返します。

        Returns:
            str: モールス表現です。
        """
        return self.__morse_code

    def play(self, repeat: int = 1, BT: bool = False, AR: bool = False):
        """モールス信号音を再生します。

        Args:
            repeat (int, optional): 本文の繰り返し再生数です。
            BT (bool, optional): 送信開始の合図を再生するかどうかです。
            AR (bool, optional): 送信終了の合図を再生するかどうかです。
        """
        n = self.minimum_length
        ct = C2M_TABLE
        sep_dot = n / 1000
        sep_word = sep_dot * 7
        sep_char = sep_dot * 3
        fq = self.frequency
        text = ' '.join([self.text for _ in range(repeat)])
        if BT:
            text = '= ' + text
        if AR:
            text += ' +'
        for i, char in enumerate(text):
            if char == ' ':
                time.sleep(sep_word)
                continue
            elif i:
                time.sleep(sep_char)
            for j, dot in enumerate(ct[char]):
                if j:
                    time.sleep(sep_dot)
                if dot:
                    Beep(fq, n * 3)
                else:
                    Beep(fq, n)

    @classmethod
    def parse_morse(cls,
                    code: str,
                    *,
                    short: str = '.',
                    long: str = '-',
                    sep: str = ' ',
                    frequency: int = 440,
                    minimum_length: int = 100) -> 'MorseCode':
        if len({short, long, sep, ' '}) > 4:
            msg = '3種類以上の文字を使用することはできません。'
            raise ValueError(msg)
        if len({short, long, sep}) != 3:
            msg = 'short, long, sepはそれぞれ違う文字である必要があります。'
            raise ValueError(msg)
        char = code.split(sep)
        table = M2C_TABLE
        text = []
        for c in char:
            if c == '':
                if text[-1] == ' ':
                    continue
                text.append(' ')
                continue
            pattern = []
            for p in c:
                if p == long:
                    pattern.append(1)
                elif p == short:
                    pattern.append(0)
                else:
                    msg = f'"{code}"をモールス信号として解釈できませんでした。'
                    raise ValueError(msg)
            text.append(table[tuple(pattern)])
        text = ''.join(text)
        return MorseCode(text, short=short, long=long, sep=sep, frequency=frequency, minimum_length=minimum_length)
