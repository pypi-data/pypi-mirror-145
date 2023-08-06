import argparse
from unittest import TestCase, main, mock

from incase import parse_args, cli


class TestCLI(TestCase):
    def test_argparser(self):
        args = parse_args(["some word", "--case", "upper"])
        self.assertEqual(args.words[0], "some word")
        self.assertEqual(args.case, "upper")

    @mock.patch("builtins.print")
    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(words=["this"], case="upper"),
    )
    def test_cli(self, mock_args, mock_print):
        cli()
        mock_print.assert_called_with("THIS")


if __name__ == "__main__":
    main()  # pragma: no cover
