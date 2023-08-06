import pyfiglet
from rich import print


class ASCII():
    """docstring for ASCII"""

    def __init__(self):
        pass

    def text(str, font='', color='white'):
        if font:
            ascii_text = pyfiglet.figlet_format(str, font=font)
            print(f'[{color}]{ascii_text}[/{color}]')
        else:
            ascii_text = pyfiglet.figlet_format(str)
            print(f'[{color}]{ascii_text}[/{color}]')
