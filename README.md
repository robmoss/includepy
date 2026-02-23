# Include Python source code in Markdown files

[![Latest version](https://badge.fury.io/py/includepy.svg)](https://pypi.org/project/includepy/)
[![Documentation](https://readthedocs.org/projects/includepy/badge/)](https://includepy.readthedocs.io/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)

The `includepy` package provides a Markdown preprocessor that allows you to include the source code for a specific Python object (e.g., a function or class) when rendering Markdown content.

For example, to include the source code for the `factorial` function in `tests/example.py`, add the following lines in a code block:

```py
-->includepy<-- tests/example.py
-->pyobject<-- factorial
```

The `includepy` preprocessor will turn this into the following:

```py
def factorial(n: int) -> int:
    value = n  # (1)
    while n > 1:
        n -= 1
        value *= n
    return value
```

See the [documentation](https://includepy.readthedocs.io/) for further details.
