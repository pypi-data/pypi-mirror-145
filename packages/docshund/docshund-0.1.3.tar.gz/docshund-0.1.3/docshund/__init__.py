#!/usr/bin/env python3
"""
A module for building documentation in Markdown form from a Python file.

Simple, no-frills. Uses Google-style docstrings.
"""

from typing import List

import re

_HEADER = r"\b(\w+):$"
_ARGUMENT = r"\b(\S+)(?:\s\((\S+)(?:\:\s(\S+))?\))?:\s+(.*)"
_DOCUMENTED_ENTITY = re.compile(
    r'''(class|def) (.+?)(\((.*?)\))?:\n\s+"""((?:.*?\n)+?\s*)"""$''',
    # re.MULTILINE and re.DOTALL
    re.MULTILINE | re.DOTALL,
)

__version__ = "0.1.3"


class Section:
    """
    A Section represents the content of a single Python entity.

    This includes classes, functions, and class methods.
    """

    def __init__(self, title: str = None, contents=None) -> None:
        """
        Create a new Section with a title and content string.

        Arguments:
            title (str: None): The title of the section. Optional
            contents (str: None): The contents of the section. Optional

        Returns:
            None

        """
        self.title = title
        self.contents = contents

    def to_markdown(self) -> str:
        """
        Convert the section to Markdown.

        Arguments:
            None

        Returns:
            str: A markdown representation of the section.

        """
        md = ""

        if self.title:
            md += f"# {self.title}"

        if self.contents:
            md += self.contents

        return md


class Report:
    """
    A complete report of a Python file, containing all Sections.

    """

    def __init__(self, sections: List[Section] = None) -> None:
        """
        Create a new Report with a list of Sections.

        Arguments:
            sections (List[Section]: None): An optional list of sections to
                include in the report.

        Returns:
            None

        """
        if sections is None:
            sections = []
        self.sections = sections

    def to_markdown(self) -> str:
        """
        Convert the entire report to Markdown.

        Arguments:
            None

        Returns:
            str: A markdown representation of the report.

        """
        return "\n".join([s.to_markdown() for s in self.sections])

    def add_section(self, section: Section, pos: int = -1) -> None:
        """
        Add a section to the report, optionally at a given position.

        Arguments:
            section (Section): The section to insert
            pos (int: -1): The index at which to insert the new section. If
                none is provided, the default is to add the section to the
                end of the report.

        Returns:
            None

        """
        if pos:
            self.sections.insert(pos, section)
        else:
            self.sections.append(section)


class Docshund:
    """
    The high-level class for generating documentation.

    This is what you should call if you are trying to generate documentation
    programmatically (or from the command line).
    """

    def __init__(self, **kwargs) -> None:
        """
        Create a new Docshund documentation engine.

        Arguments:
            language (None): The language to use. This is currently not used,
                but will ultimately provide support for different programming
                languages than Python.
            indent (str: "    "): The default indentation level for the file.
                Defaults to four spaces.

        Returns:
            None

        """

        self._language = kwargs.get("language", None)

        if self._language is None:
            pass
            # self._infer_language()

        self._indent_string = kwargs.get("indent", (" " * 4))

    def _get_indent_level(self, line: str) -> int:
        """
        Return the indent level, based upon the left spacing.

        Arguments:
            line (str): The line to guess indentation for.

        Returns:
            int: The guessed indentation level of the line of code

        """
        return len(line) - len(line.lstrip(self._indent_string))

    def _clean_docstring(self, docstring: str) -> List[str]:
        """
        Clean a docstring, reducing indentation where necessary.

        Arguments:
            docstring (str): The complete docstring from the code src

        Returns:
            List[str]: A list of strings, one for each line of the cleaned
                docstring output.

        """
        doclines = docstring.split("\n")
        base_indentation = (
            self._get_indent_level(doclines[0])
            if (self._get_indent_level(doclines[0]))
            else self._get_indent_level(doclines[1])
        )
        doclines = [d[base_indentation:] for d in doclines]

        reflowed: List[str] = []
        last_indentation = base_indentation
        for line in doclines:
            if (
                # Line has contents:
                line != ""
                # Line is indented the same as previous:
                and self._get_indent_level(line) == last_indentation
                # Line is not argument-like:
                and len(list(re.finditer(_ARGUMENT, line))) == 0
            ):
                reflowed[-1] += " " + line
            else:
                reflowed.append(line)
                if line == "":
                    last_indentation = -1
                else:
                    last_indentation = self._get_indent_level(line)
        return [(line).replace(">>>", "\>>>") for line in reflowed]

    def parse_docstring(self, docstring: str) -> str:
        """
        Parse a single docstring, converting from original text to Markdown.

        Arguments:
            docstring (str): The docstring from the code src

        Returns:
            str: The parsed markdown output

        """
        report = []
        description = None

        doclines = self._clean_docstring(docstring)

        for line in doclines:

            is_header = list(re.finditer(_HEADER, line))
            is_arg = list(re.finditer(_ARGUMENT, line))
            if len(is_header):
                report.append("### " + is_header[0].groups()[0])
            elif len(is_arg):
                varname, type, default, description = is_arg[0].groups()
                report.append(
                    f"> - **{varname}** (`{type}`: `{default}`): {description}"
                )

            else:
                report.append(line)

        return "\n".join([r.rstrip() for r in report])

    def parse_document(self, document: str) -> str:
        """
        Parse a full document, and generate markdown.

        Arguments:
            document (str): The document to parse; i.e. contents of src file

        Returns:
            str: The documentation, in markdown form

        """
        documentation = []
        entities = list(re.finditer(_DOCUMENTED_ENTITY, document))
        for e in entities:
            grps = e.groups()
            if len(grps) == 5:
                type, signature, _, args, doc = e.groups()
            type = {"def": "Function", "class": "Class"}[type]
            if type == "Function":
                fnarg = " ".join(args.split())
                documentation.append(
                    "\n".join(
                        [
                            f"### *{type}* `{signature} ({fnarg})`",
                            "",
                            self.parse_docstring(doc),
                        ]
                    )
                )
            else:
                documentation.append(
                    "\n".join(
                        [
                            f"## *{type}* `{signature}`",
                            "",
                            self.parse_docstring(doc),
                        ]
                    )
                )
        return "\n\n".join(documentation)
