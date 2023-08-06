import re
from typing import Any, Callable, Tuple


class Text:
    """Contain that contains string manipulation utilities"""

    BOLD = "\033[1m"
    BOLD_END = "\033[0m"

    @staticmethod
    def lower(text: str) -> str:
        return text.lower()

    @staticmethod
    def split_capitals(text: str, sep: str = ' ') -> str:
        return sep.join(re.findall(".[^A-Z]*", text))

    @staticmethod
    def split_capitals_with_underscore(text: str) -> str:
        return "_".join(re.findall(".[^A-Z]*", text))

    @staticmethod
    def split(text: str, sep: str = ' ') -> str:
        return text.split(sep)

    @staticmethod
    def get(texts: str, index: int = 0) -> str:
        return texts[index]


def chain_functions(x: Any, *functions: Tuple[Callable]) -> Any:
    """Given a list of functions chains them over input x"""

    for function in functions:
        x = function(x)
    return x
