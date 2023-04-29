"""Extension for Code Outline.

See extend.txt for more details on creating an extension.
See config-extension.def for configuring an extension.
"""

from idlelib.config import idleConf
from functools import wraps


def format_selection(format_line):
    "Apply a formatting function to all of the selected lines."

    @wraps(format_line)
    def apply(self, event=None):
        head, tail, chars, lines = self.formatter.get_region()
        for pos in range(len(lines) - 1):
            line = lines[pos]
            lines[pos] = format_line(self, line)
        self.formatter.set_region(head, tail, chars, lines)
        return 'break'

    return apply


class CodeOutline:
    """Show code outline with class and method names."""

    # Extend the options menu.
    menudefs = [
        ('options', [
            ('Show Code Outline', '<<show-code-outline>>'),
        ] )
    ]

    def __init__(self, editwin):
        "Initialize the settings for this extension."
        self.editwin = editwin
        self.text = editwin.text
        self.formatter = editwin.fregion

    @classmethod
    def reload(cls):
        "Load class variables from config."
        cls.code_outline_text = idleConf.GetOption('extensions', 'CodeOutline', 'code-outline-text')

    @format_selection
    def show_code_outline_event(self, line):
        """Insert text CO (for code outline) at the beginning of each selected line.

        This is bound to the <<show-code-outline>> virtual event when the extensions
        are loaded.
        """
        return f'{self.code_outline_text}{line}'


CodeOutline.reload()


if __name__ == "__main__":
    import unittest
    unittest.main('idlelib.idle_test.test_zzdummy', verbosity=2, exit=False)
