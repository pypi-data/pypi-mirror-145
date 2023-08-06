from rich import print


class Color():

    def __init__(self, text_color='white'):
        self.text_color = text_color

    def error(self, msg='Lorem Ipsum', color='red'):
        """Prints on the console: [X] {msg}"""
        print(f'[[{color}]X[/{color}]] [{self.text_color}]{msg}[/{self.text_color}]')

    def warning(self, msg='Lorem Ipsum', color='yellow'):
        """Prints on the console: [!] {msg}"""
        print(f'[[{color}]![/{color}]] [{self.text_color}]{msg}[/{self.text_color}]')

    def info(self, msg='Lorem Ipsum', color='white'):
        """Prints on the console: [i] {msg}"""
        print(f'[[{color}]i[/{color}]] [{self.text_color}]{msg}[/{self.text_color}]')

    def custom(self, msg='Lorem Ipsum', symbol='*', color='white'):
        print(f'[[{color}]{symbol}[/{color}]] [{self.text_color}]{msg}[/{self.text_color}]')
