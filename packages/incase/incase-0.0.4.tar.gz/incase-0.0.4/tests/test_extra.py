from types import GeneratorType
from unittest import TestCase, main

from black import assert_equivalent

from incase import Case, case_modifier, incase, planetary_defense_shield


class TestExtra(TestCase):
    def test_incase_str_str(self):
        self.assertEqual(incase("snake", "example text"), "example_text")

    def test_incase_str_list(self):
        self.assertEqual(
            incase("upper", ["three", "word", "list"]), ["THREE", "WORD", "LIST"]
        )

    def test_incase_str_tuple(self):
        self.assertEqual(
            incase("upper", ("three", "word", "tuple")), ("THREE", "WORD", "TUPLE")
        )

    def test_incase_str_generator(self):
        generator = (word for word in ["some", "list"])
        incased = incase("upper", generator)
        self.assertIsInstance(incased, GeneratorType)
        self.assertEqual(list(incased), ["SOME", "LIST"])

    def test_incase_str_nested(self):
        nested = {
            "first_key": ["some", "list"],
            "second_key": {"another": "dict"},
            "third_key": 1,
        }
        self.assertEqual(
            incase("upper", nested),
            {
                "first_key": ["SOME", "LIST"],
                "second_key": {"another": "DICT"},
                "third_key": 1,
            },
        )

    def test_incase_mapping_list(self):
        self.assertEqual(
            incase(["upper", "lower", "snake", "camel"], ["some_word"] * 4),
            ["SOME WORD", "some word", "some_word", "someWord"],
        )

    def test_incase_mapping_dict(self):
        self.assertEqual(
            incase(
                {"first_key": "alternating", "second_key": "title"},
                {"first_key": "some example", "second_key": "another example"},
            ),
            {"first_key": "SoMe eXaMpLe", "second_key": "Another Example"},
        )

    def test_incase_mapping_str(self):
        self.assertEqual(incase({"bob": "upper"}, "bob"), "BOB")

    def test_incase_case_none(self):
        self.assertIsNone(incase("upper", None))

    def test_incase_none_none(self):
        self.assertIsNone(incase(None, None))

    def test_incase_case_str(self):
        self.assertEqual(incase(Case.UPPER, "this"), "THIS")

    def test_incase_exception(self):
        with self.assertRaises(NotImplementedError):
            incase(1, "test")

    def test_case_modifier(self):
        @case_modifier(
            args_case="upper",
            keywords_case="snake",
            kwargs_case="upper",
            output_case="upper",
        )
        def test_func(arg1, *, kwarg_1, **kwargs):
            self.assertEqual(arg1, arg1.upper())
            self.assertEqual(kwarg_1, kwarg_1.upper())
            for kwarg_name in kwargs.keys():
                self.assertEqual(kwarg_name, kwarg_name.lower())
            return "test"

        result = test_func("something lower", kwarg_1="also lower", KWARG_2=None)
        self.assertEqual(result, "TEST")

    def test_planetary_defense(self):
        values_dict = {"thing": "stuff"}
        planetary_defense_shield("upper", values_dict)
        self.assertEqual(values_dict["thing"], values_dict["THING"])


if __name__ == "__main__":
    main()  # pragma: no cover
