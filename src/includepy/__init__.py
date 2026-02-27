"""
A Markdown extension that inserts code for Python objects (such as functions
and classes).
"""

import ast
import re
import textwrap

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor
from pathlib import Path
from typing import Any

# The groups are:
# 1. Indentation
# 2. Escaping
# 3. Option name
# 4. Option value
RE_OPTION = re.compile(
    r"^([ \t]*)(;*)-->([a-zA-Z0-9-_]+)<--[ \t]*(\S+)[ \t]*$"
)

# Match any of "m-n", "m-", "-n", "n".
RE_LINERANGE = re.compile(r"^([0-9]+-[0-9+]|[0-9]+-|-[0-9]+|[0-9])+$")


def valid_options() -> set[str]:
    """
    Returns the valid option names.
    """
    return set(default_options()) | {"pyobject"}


def default_options() -> dict[str, str]:
    """
    Returns default values for options that have defaults.
    """
    return {
        "lines_before": "0",
        "lines_after": "0",
        "extra_indent": "0",
        "only_lines": "",
    }


def find_object(name: str | None, node: ast.AST) -> ast.AST:
    """
    Find a named object (e.g., function or class) in a syntax tree.
    """
    if name is None:
        raise IncludePyError("No Python object specified")

    # NOTE: we support nested names ("a.b.c").
    name_parts = name.split(".")

    for ix, name_part in enumerate(name_parts):
        body = getattr(node, "body", [])
        matches = [n for n in body if getattr(n, "name", None) == name_part]
        if len(matches) != 1:
            frag = ".".join(name_parts[: ix + 1])
            raise IncludePyError(f"Found {len(matches)} matches for {frag}")
        node = matches[0]

    return node


def selected_lines(input_lines: list[str], only_lines: str) -> list[str]:
    """
    Return only selected lines from a code block.

    Parameters
    ----------
    input_lines : list[str]
        The input lines of text.
    only_lines : str
        A string that contains one or more line-range specifiers, separated by
        commas.
        Each specifier must have one of the following forms: ``n`` for the
        ``nth`` input line, ``n-`` for every line from the ``nth`` to the end,
        ``-n`` for every line from the start up to the ``nth``, or ``n-p`` for
        every line from the ``nth`` up to the ``pth``.
        Note that line numbering begins at ``1``.

    Returns
    -------
    list[str]
        The selected lines of text.
    """
    line_ranges = only_lines.split(",")
    lr_matches = [RE_LINERANGE.match(lr) for lr in line_ranges]

    output_lines = []

    for lr in lr_matches:
        if lr is None:
            raise IncludePyError("Invalid only_lines: {only_lines}")

        bounds = tuple(lr.group(0).split("-"))
        try:
            match bounds:
                case (only,):
                    ix = int(only) - 1
                    output_lines.append(input_lines[ix])
                case (start, ""):
                    ix = int(start) - 1
                    output_lines.extend(input_lines[ix:])
                case ("", end):
                    ix = int(end)
                    output_lines.extend(input_lines[:ix])
                case (start, end):
                    a = int(start) - 1
                    b = int(end)
                    output_lines.extend(input_lines[a:b])
                case _:
                    raise ValueError(bounds)
        except (ValueError, IndexError) as e:
            raise IncludePyError(f"Invalid only_lines: {lr.group(0)}") from e

    return output_lines


class ProcessorState:
    """
    Define an interface for processing Markdown lines.
    """

    def read_line(
        self, input_line: str | None, output_lines: list[str]
    ) -> "ProcessorState":
        """
        Process an input line and return the updated processor state.

        Parameters
        ----------
        input_line : str | None
            A line of text, or ``None`` to indicate the end of the file.
        output_lines: list[str]
            The output Markdown lines, can be mutably updated.

        Returns
        -------
        ProcessorState
            The new state of the IncludePy processor.
        """
        return self  # pragma: no cover


class EchoLines(ProcessorState):
    """
    Preserve existing Markdown content.
    """

    def read_line(
        self, input_line: str | None, output_lines: list[str]
    ) -> ProcessorState:
        if input_line is None:
            return self
        re_match = RE_OPTION.match(input_line)
        if not re_match:
            output_lines.append(input_line)
            return self
        elif re_match.group(2):
            output_lines.append(input_line.replace(";", "", 1))
            return self
        else:
            return ParseBlock(re_match)


class ParseBlock(ProcessorState):
    """
    Parse an IncludePy block and add the specified Python code to the output.
    """

    def __init__(self, re_match: re.Match[str]):
        # 1. Indentation
        # 2. Escaping
        # 3. Option name
        # 4. Option value
        escaping = re_match.group(2)
        if escaping:
            raise IncludePyError("Should not parse an escaped line")
        opt_name = re_match.group(3)
        if opt_name != "includepy":
            raise IncludePyError(
                f"Expected 'includepy' but found '{opt_name}'"
            )
        self.indent_str = re_match.group(1)
        self.python_file = Path(re_match.group(4))
        self.defaults = default_options()
        self.options: dict[str, str] = {}

    def read_line(
        self, input_line: str | None, output_lines: list[str]
    ) -> ProcessorState:
        if input_line is None:
            re_match = None
        else:
            re_match = RE_OPTION.match(input_line)

        if not re_match or re_match.group(2):
            # Extract the source code and add to `output_lines`, and then
            # process the current input line.
            self.add_code_lines(output_lines)
            next_state = EchoLines()
            return next_state.read_line(input_line, output_lines)
        elif re_match and re_match.group(3) == "includepy":
            # Extract the source code and add to `output_lines`, then start
            # parsing the next block.
            self.add_code_lines(output_lines)
            return ParseBlock(re_match)

        # Continue parsing the option lines.
        escaping = re_match.group(2)
        if escaping:
            raise IncludePyError("Should not parse an escaped line")
        opt_name = re_match.group(3)
        opt_value = re_match.group(4)
        if opt_name in self.options:
            raise IncludePyError(f"Duplicate option {opt_name}")
        if opt_name not in valid_options():
            raise IncludePyError(f"Invalid option {opt_name}")
        self.options[opt_name] = opt_value

        return self

    def add_code_lines(self, output_lines: list[str]) -> None:
        options = self.defaults | self.options

        with open(self.python_file) as f:
            source_lines = f.readlines()
            module: ast.AST = ast.parse("".join(source_lines))

        obj_name = options.get("pyobject")
        obj = find_object(obj_name, module)

        if hasattr(obj, "lineno"):
            lineno = obj.lineno
        else:
            raise IncludePyError("No line number in syntax tree")
        if hasattr(obj, "end_lineno"):
            end_lineno = obj.end_lineno
            if end_lineno is None:
                raise IncludePyError(
                    f"no end line for {obj_name} in {self.python_file}"
                )
        else:
            raise IncludePyError("No end line number in syntax tree")

        try:
            n_back = int(options["lines_before"])
        except ValueError:
            raise IncludePyError(
                "lines_before must be a valid integer"
            ) from None
        if n_back < 0:
            raise IncludePyError("lines_before cannot be negative")

        try:
            n_fwd = int(options["lines_after"])
        except ValueError:
            raise IncludePyError(
                "lines_after must be a valid integer"
            ) from None
        if n_fwd < 0:
            raise IncludePyError("lines_after cannot be negative")

        try:
            n_indent = int(options["extra_indent"])
        except ValueError:
            raise IncludePyError(
                "extra_indent must be a valid integer"
            ) from None
        if n_indent < 0:
            raise IncludePyError("extra_indent cannot be negative")

        indent_str = self.indent_str
        if n_indent > 0:
            indent_str = self.indent_str + n_indent * " "

        start_ix = max(0, lineno - 1 - n_back)
        end_ix = min(len(source_lines), end_lineno + n_fwd)
        obj_lines = source_lines[start_ix:end_ix]

        # NOTE: remove any code indentation (e.g., class methods).
        obj_lines = textwrap.dedent("".join(obj_lines)).split("\n")
        # Remove the trailing empty line after the final newline.
        obj_lines = obj_lines[:-1]

        # Retain only selected lines if "only_lines" is defined.
        only_lines = options["only_lines"]
        if only_lines:
            obj_lines = selected_lines(obj_lines, only_lines)

        # Add the source lines to the document.
        # NOTE: we need to indent and strip newlines.
        code_lines = [
            indent_str + obj_line.rstrip() for obj_line in obj_lines
        ]
        output_lines.extend(code_lines)


class IncludePyError(Exception):
    """
    Raised when an error is encountered while attempting to insert the code
    for a Python object.
    """


class IncludePyProc(Preprocessor):
    """The IncludePy preprocessor."""

    def __init__(self, config: dict[str, Any], md: Markdown):
        # NOTE: refer to the Extensions API for configuration settings:
        # https://python-markdown.github.io/extensions/api/#configsettings
        super().__init__()

    def run(self, lines: list[str]) -> list[str]:
        """
        Process the input Markdown content and include Python source code as
        directed.

        Parameters
        ----------
        lines : list[str]
            A list of text lines.

        Returns
        -------
        list[str]
            The processed lines of text, with Python source code lines added
            as directed.
        """
        output_lines: list[str] = []
        state: ProcessorState = EchoLines()

        for line in lines:
            state = state.read_line(line, output_lines)
        state.read_line(None, output_lines)

        return output_lines


class IncludePy(Extension):
    """The IncludePy extension class."""

    def __init__(self, **kwargs: dict[str, Any]):
        # Define the default configuration settings.
        self.config = {
            "priority": [100, "Default priority for IncludePy"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        """
        Register this extension with a Markdown processor.

        Parameters
        ----------
        md : markdown.core.Markdown
             A Markdown processor.

        Returns
        -------
        None
        """
        md.registerExtension(self)
        config = self.getConfigs()
        proc = IncludePyProc(config, md)
        # NOTE: we need a higher priority (larger number) than both of
        # `pymdownx.superfences.SuperFencesBlockPreprocessor` (25) and
        # `pymdownx.superfences.SuperFencesCodeBlockProcessor` (80).
        # Otherwise, the ">" and "<" characters will be converted into HTML
        # entities and the `IncludePyProc` preprocessor will have no effect.
        # See
        # https://github.com/EastSunrise/mkdocs-graphviz/blob/main/mkdocs_graphviz.py
        # for examples of using configuration settings.
        md.preprocessors.register(
            item=proc, name="includepy", priority=config["priority"]
        )


def makeExtension(**kwargs: dict[str, Any]) -> IncludePy:
    """Return an instance of the IncludePy extension."""
    return IncludePy(**kwargs)
