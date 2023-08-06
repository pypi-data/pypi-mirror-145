import enum
import re
import typing as t
from collections import UserString


WHITESPACE = re.compile(r"\s|-")
UPPER_DELIMITED_TO_SNAKE_1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
UPPER_DELIMITED_TO_SNAKE_2 = re.compile(r"([a-z\d])([A-Z])")
UPPER_DELIMITED_TO_SNAKE_REPL = r"\1_\2"


class Case(enum.Enum):
    CASELESS = 0
    CAMEL = 1
    DROMEDARY = 1
    MEDIAL = 1
    SNAKE = 2
    PASCAL = 3
    INITIAL_CAPITALS = 3
    KEBAB = 4
    DASH = 4
    UPPER_SNAKE = 5
    UPPERCASE = 6
    UPPER = 6
    LOWERCASE = 7
    LOWER = 7
    TITLE = 8
    ALTERNATING = 9
    SARCASM = 9
    ORIGINAL = 10
    WORD = 11


class Caseless(str, UserString):
    def snakify(self, string: str) -> str:
        # Trim, Replace whitespace and - with _
        string = WHITESPACE.sub("_", string.strip())
        # Camel/Pascal to snake and lowercase
        return UPPER_DELIMITED_TO_SNAKE_2.sub(
            UPPER_DELIMITED_TO_SNAKE_REPL,
            UPPER_DELIMITED_TO_SNAKE_1.sub(UPPER_DELIMITED_TO_SNAKE_REPL, string),
        ).lower()

    @property
    def parts(self):
        return self.snakify(self.data).split("_")

    @property
    def snake(self) -> str:
        return "_".join(self.parts)

    @property
    def upper_snake(self) -> str:
        return self.snake.upper()

    @property
    def kebab(self) -> str:
        return self.snake.replace("_", "-")

    @property
    def upper(self) -> str:
        return self.word.upper()

    @property
    def lower(self) -> str:
        return self.word.lower()

    @property
    def title(self) -> str:
        return self.word.title()

    @property
    def camel(self) -> str:
        return "".join([self.parts[0], *[word.title() for word in self.parts[1:]]])

    @property
    def pascal(self) -> str:
        return "".join([word.title() for word in self.parts])

    @property
    def alternating(self):
        uppercase = [word.upper() for word in self.word[0::2]]
        lowercase = [word.lower() for word in self.word[1::2]]
        return "".join([val for pair in zip(uppercase, lowercase) for val in pair]) + (
            self.word[-1] if len(self.word) % 2 == 1 else ""
        )

    @property
    def original(self):
        return self.data

    @property
    def word(self) -> str:
        return " ".join(self.parts)

    def __getitem__(self, key: int | slice | str | Case) -> str:
        if isinstance(key, (int, slice)):
            return self.data[key]

        if isinstance(key, str):
            key = Case[key.upper()]

        match key:
            case Case.CASELESS:
                return self
            case Case.CAMEL:
                return self.camel
            case Case.SNAKE:
                return self.snake
            case Case.PASCAL:
                return self.pascal
            case Case.KEBAB:
                return self.kebab
            case Case.UPPER_SNAKE:
                return self.upper_snake
            case Case.UPPERCASE:
                return self.upper
            case Case.LOWERCASE:
                return self.lower
            case Case.TITLE:
                return self.title
            case Case.ALTERNATING:
                return self.alternating
            case Case.ORIGINAL:
                return self.original
            case Case.WORD:
                return self.word

    def __eq__(self, other):
        return self.parts == Caseless(other).parts

    def __repr__(self) -> str:
        return f'Caseless("{self.data}")'

    def __hash__(self) -> str:
        return hash(tuple(self.parts))

    @classmethod
    def factory(cls, case: str | Case) -> t.Callable[[str], str]:
        def factory_func(word: str) -> str:
            return cls(word)[case]

        return factory_func
