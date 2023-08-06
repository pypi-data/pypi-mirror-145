import re
import typing as t
import enum

WHITESPACE = re.compile(r"\s")
UPPER_DELIMITED_TO_SNAKE_1 = re.compile(r"(.)([A-Z][a-z]+)")
UPPER_DELIMITED_TO_SNAKE_2 = re.compile(r"([a-z0-9])([A-Z])")
UPPER_DELIMITED_TO_SNAKE_REPL = r"\1_\2"


class Case(enum.Enum):
    CASELESS = 0
    CAMEL = 1
    SNAKE = 2
    PASCAL = 3
    WORD = 4
    UPPER_SNAKE = 5
    UPPERCASE = 6
    UPPER = 6
    LOWERCASE = 7
    LOWER = 7
    TITLE = 8
    ALTERNATING = 9
    SARCASM = 9
    ORIGINAL = 10


class Caseless:
    parts: tuple
    _origin: str

    def __init__(
        self, name: t.Union[str, "Caseless", None], parts: t.Tuple[str] = None
    ):
        if isinstance(name, Caseless):
            parts, self._origin = name.parts, name._origin
        else:
            self._origin = name
        if not parts:
            parts = tuple(self.snakify(name).split("_"))
        self.parts = parts

    @staticmethod
    def snakify(string: str) -> str:
        # Trim, Replace whitespace with _
        string = WHITESPACE.sub("_", string.strip())
        # Camel/Pascal to snake and lowercase
        return UPPER_DELIMITED_TO_SNAKE_2.sub(
            UPPER_DELIMITED_TO_SNAKE_REPL,
            UPPER_DELIMITED_TO_SNAKE_1.sub(UPPER_DELIMITED_TO_SNAKE_REPL, string),
        ).lower()

    @property
    def snake(self) -> str:
        return "_".join(self.parts)

    @property
    def upper_snake(self) -> str:
        return self.snake.upper()

    @property
    def word(self) -> str:
        return " ".join(self.parts)

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
        return "".join([val for pair in zip(uppercase, lowercase) for val in pair])

    def __getitem__(self, case: str | Case) -> str:
        if isinstance(case, str):
            case = Case[case.upper()]

        match case:
            case Case.CASELESS:
                return self
            case Case.CAMEL:
                return self.camel
            case Case.SNAKE:
                return self.snake
            case Case.PASCAL:
                return self.pascal
            case Case.WORD:
                return self.word
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
                return self._origin

    def __eq__(self, other):
        return self.parts == Caseless(other).parts

    def __repr__(self) -> str:
        return f"Caseless(parts={self.parts})"

    def __str__(self) -> str:
        return f'Casless("{self.word}")'

    @classmethod
    def factory(cls, case: str | Case) -> t.Callable[[str], str]:
        def factory_func(word: str) -> str:
            return cls(word)[case]

        return factory_func
