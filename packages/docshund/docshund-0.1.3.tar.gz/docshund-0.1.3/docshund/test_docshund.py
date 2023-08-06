from docshund import Docshund
import unittest


TEST_FILE = '''

class Blah:
    """
    This is a class.

    >>> doctest.works()
    True

    """

    def __init__(self):
        """
        Create a new Blah.

        Endow it with all of the qualities that a good Blah should
        have, and then set it free.
        """
        pass

    def engage(self, friend=None):
        """
        Engage the blah to a friend.

        Arguments:
            friend (Blah: None): The friend to whom this Blah should be engaged
            use_ring (boolean: True): Whether to use a ring

        Returns:
            Blah: The new combined blah
        """
        pass

'''

MULTILINE_FUNCTION = '''

def foo(
    bar: int,
    baz: str
):
    """
    This function foos a bar for you.

    Optionally also foos a baz.

    """
    pass

'''

SINGLELINE_FUNCTION = '''
def foo(bar: int,baz: str):
    """
    This function foos a bar for you.

    Optionally also foos a baz.

    """
    pass
'''


class TestDocshund(unittest.TestCase):
    def test_clean_linebreaks(self):
        ds = """\
        This is a docstring.

        Here is a long description that
        spans many lines.
        """

        D = Docshund()
        self.assertEqual(
            D._clean_docstring(ds),
            [
                "This is a docstring.",
                "",
                "Here is a long description that spans many lines.",
                "",
            ],
        )

    def test_description_only_docstring(self):
        ds = """\
        This is a single-line description.

        It even spans multiple lines, which is great. I
        love that.

        But there's another part.

        Arguments:
            test (int: 1): Frogs!
        """

        D = Docshund()
        self.assertEqual(
            D.parse_docstring(ds),
            "This is a single-line description.\n"
            "\n"
            "It even spans multiple lines, which is great. I love that.\n"
            "\n"
            "But there's another part.\n"
            "\n"
            "### Arguments\n"
            "> - **test** (`int`: `1`): Frogs!\n",
        )

    def test_parse_document(self):
        D = Docshund()
        parsed_doc = D.parse_document(TEST_FILE)
        self.assertIn("Create a new Blah", parsed_doc)

    def test_parse_arguments(self):
        D = Docshund()
        parsed_doc = D.parse_document(TEST_FILE)

        self.assertIn(
            "> - **friend** (`Blah`: `None`): The friend to whom this Blah should be engaged",
            parsed_doc,
        )
        self.assertIn(
            "> - **use_ring** (`boolean`: `True`): Whether to use a ring", parsed_doc
        )

    def test_parse_doctest(self):
        D = Docshund()
        parsed_doc = D.parse_document(TEST_FILE)

        self.assertIn(
            "\\>>>",
            parsed_doc,
        )

    def test_multiline_function(self):
        D = Docshund()
        parsed_doc = D.parse_document(MULTILINE_FUNCTION)

        self.assertIn(
            "foo (bar: int, baz: str)",
            parsed_doc,
        )
