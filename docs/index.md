---
icon: lucide/rocket
---

# Get started

The `includepy` package provides a Markdown preprocessor that allows you to include the source code for a specific Python object (e.g., a function or class) when rendering Markdown content.

!!! note

    This extension works with all of the standard [code block features](https://zensical.org/docs/authoring/code-blocks/), such as line numbering, line highlighting, and code annotations.
    See [Including a function](#including-a-function) for an example.

## Installation

Install `includepy` with pip:

```sh
pip install includepy
```

## Configuration

Add the following settings to your [Zensical](https://zensical.org/) or [MkDocs](https://www.mkdocs.org/) configuration:

=== "`zensical.toml`"

    ```toml
    [project.markdown_extensions.includepy]
    ```

=== "`mkdocs.yml`"

    ```yaml
    markdown_extensions:
      - includepy
    ```

## Example Python file

We use the following `example.py` file in the examples below:

```py title="example.py"
--8<-- "example.py"
```

## Including a function

If you write the following Markdown:

~~~md
```py title="The factorial function", linenums="1", hl_lines="3-5"
;-->includepy<-- example.py
;-->pyobject<-- factorial
```

1. This is a code annotation.
~~~

You will get the following HTML:

```py title="The factorial function", linenums="1", hl_lines="3-5"
-->includepy<-- example.py
-->pyobject<-- factorial
```

1. This is a code annotation.

## Including a class

If you write the following Markdown:

~~~md
```py
;-->includepy<-- example.py
;-->pyobject<-- MyClass
```
~~~

You will get the following HTML:

```py
-->includepy<-- example.py
-->pyobject<-- MyClass
```

## Including a class method

If you write the following Markdown:

~~~md
```py
;-->includepy<-- example.py
;-->pyobject<-- MyClass.do_thing
```
~~~

You will get the following HTML:

```py
-->includepy<-- example.py
-->pyobject<-- MyClass.do_thing
```

## Adding content before/after

If you write the following Markdown:

~~~md
```py
x = 1
;-->includepy<-- example.py
;-->pyobject<-- factorial
y = 2
```
~~~

You will get the following HTML:

```py
x = 1
-->includepy<-- example.py
-->pyobject<-- factorial
y = 2
```

## Including only a subset of lines

If you write the following Markdown:

~~~md
```py
;-->includepy<-- example.py
;-->pyobject<-- factorial
;-->only_lines<-- 1,3-4,-2,5-
```
~~~

You will get the following HTML:

```py
def factorial(n: int) -> int:
    while n > 1:
        n -= 1
def factorial(n: int) -> int:
    value = n  # (1)
        value *= n
    return value
```

The [``only_lines`` option](options.md) accepts one or more line ranges, separated by commas, and each line range can take any of the following forms:

- `"n"`: Line number `n`;
- `"m-n"`: All lines from number `m` to number `n` (inclusive);
- `"m-"`: All lines from number `m` to the end (inclusive); and
- `"-n"`: All lines from the start to line number `n` (inclusive).

Note that line numbers start at 1.

## Adding extra indentation

If you write the following Markdown:

~~~md
```py
;-->includepy<-- example.py
;-->pyobject<-- factorial
;-->extra_indent<-- 4
```
~~~

You will get the following HTML:

```py
-->includepy<-- example.py
-->pyobject<-- factorial
-->extra_indent<-- 4
```

## Including extra lines

If you write the following Markdown:

~~~md
```py
;-->includepy<-- example.py
;-->pyobject<-- factorial
;-->lines_before<-- 4
;-->lines_after<-- 4
```
~~~

You will get the following HTML:

```py
-->includepy<-- example.py
-->pyobject<-- factorial
-->lines_before<-- 4
-->lines_after<-- 4
```

!!! note

    Extra lines will be truncated if they would extend before the first line or after the final line of the source file.

If you write the following Markdown:

~~~md
```py
;-->includepy<-- example.py
;-->pyobject<-- something
;-->lines_before<-- 40
```
~~~

You will get the following HTML:

```py
-->includepy<-- example.py
-->pyobject<-- something
-->lines_before<-- 40
```

If you write the following Markdown:

~~~md
```py
;-->includepy<-- example.py
;-->pyobject<-- MyClass
;-->lines_after<-- 40
```
~~~

You will get the following HTML:

```py
-->includepy<-- example.py
-->pyobject<-- MyClass
-->lines_after<-- 40
```

## Nested in a list

If you write the following Markdown:

~~~md
- One thing

- Another thing:

    ```py
    ;-->includepy<-- example.py
    ;-->pyobject<-- factorial

    ;-->includepy<-- example.py
    ;-->pyobject<-- MyClass.do_thing
    ```
~~~

You will get the following HTML:

- One thing

- Another thing:

    ```py
    -->includepy<-- example.py
    -->pyobject<-- factorial

    -->includepy<-- example.py
    -->pyobject<-- MyClass.do_thing
    ```

## Escaping `includepy` blocks

If you write the following Markdown:

```md
;;-->includepy<-- example.py
;;-->pyobject<-- factorial
```

You will get the following HTML:

```md
;-->includepy<-- example.py
;-->pyobject<-- factorial
```

You can use any number of semi-colons.
For example, to show how to escape a `includepy` block you can write the following Markdown:

```md
;;;-->includepy<-- example.py
;;;-->pyobject<-- factorial
```

You will get the following HTML:

```md
;;-->includepy<-- example.py
;;-->pyobject<-- factorial
```
