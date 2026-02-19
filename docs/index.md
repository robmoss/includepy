---
icon: lucide/rocket
---

# Get started

The `includepy` package provides a Markdown preprocessor that allows you to include the source code for a specific Python object (e.g., a function or class) when rendering Markdown content.

!!! note

    This extensions works with all of the standard [code block features](https://zensical.org/docs/authoring/code-blocks/), such as line numbering, line highlighting, and code annotations.
    See [Including a function](#including-a-function) for an example.

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

We  use the `tests/example.py` file in the examples below:

```py
--8<-- "tests/example.py"
```

## Including a function

If you write the following Markdown:

~~~md
```py title="The factorial function", linenums="1", hl_lines="3-5"
;-->includepy<-- tests/example.py
;-->pyobject<-- factorial
```

1. This is a code annotation.
~~~

You will get the following HTML:

```py title="The factorial function", linenums="1", hl_lines="3-5"
-->includepy<-- tests/example.py
-->pyobject<-- factorial
```

1. This is a code annotation.

## Including a class

If you write the following Markdown:

~~~md
```py
;-->includepy<-- tests/example.py
;-->pyobject<-- MyClass
```
~~~

You will get the following HTML:

```py
-->includepy<-- tests/example.py
-->pyobject<-- MyClass
```

## Including a class method

If you write the following Markdown:

~~~md
```py
;-->includepy<-- tests/example.py
;-->pyobject<-- MyClass.do_thing
```
~~~

You will get the following HTML:

```py
-->includepy<-- tests/example.py
-->pyobject<-- MyClass.do_thing
```

## Adding content before/after

If you write the following Markdown:

~~~md
```py
x = 1
;-->includepy<-- tests/example.py
;-->pyobject<-- factorial
y = 2
```
~~~

You will get the following HTML:

```py
x = 1
-->includepy<-- tests/example.py
-->pyobject<-- factorial
y = 2
```

## Adding extra indentation

If you write the following Markdown:

~~~md
```py
;-->includepy<-- tests/example.py
;-->pyobject<-- factorial
;-->extra_indent<-- 4
```
~~~

You will get the following HTML:

```py
-->includepy<-- tests/example.py
-->pyobject<-- factorial
-->extra_indent<-- 4
```

## Including extra lines

If you write the following Markdown:

~~~md
```py
;-->includepy<-- tests/example.py
;-->pyobject<-- factorial
;-->lines_before<-- 4
;-->lines_after<-- 4
```
~~~

You will get the following HTML:

```py
-->includepy<-- tests/example.py
-->pyobject<-- factorial
-->lines_before<-- 4
-->lines_after<-- 4
```

!!! note

    Extra lines will be truncated if they would extend before the first line or after the final line of the source file.

If you write the following Markdown:

~~~md
```py
;-->includepy<-- tests/example.py
;-->pyobject<-- something
;-->lines_before<-- 40
```
~~~

You will get the following HTML:

```py
-->includepy<-- tests/example.py
-->pyobject<-- something
-->lines_before<-- 40
```

If you write the following Markdown:

~~~md
```py
;-->includepy<-- tests/example.py
;-->pyobject<-- MyClass
;-->lines_after<-- 40
```
~~~

You will get the following HTML:

```py
-->includepy<-- tests/example.py
-->pyobject<-- MyClass
-->lines_after<-- 40
```

## Nested in a list

If you write the following Markdown:

~~~md
- One thing

- Another thing:

    ```py
    ;-->includepy<-- tests/example.py
    ;-->pyobject<-- factorial

    ;-->includepy<-- tests/example.py
    ;-->pyobject<-- MyClass.do_thing
    ```
~~~

You will get the following HTML:

- One thing

- Another thing:

    ```py
    -->includepy<-- tests/example.py
    -->pyobject<-- factorial

    -->includepy<-- tests/example.py
    -->pyobject<-- MyClass.do_thing
    ```

## Escaping `includepy` blocks

If you write the following Markdown:

```md
;;-->includepy<-- tests/example.py
;;-->pyobject<-- factorial
```

You will get the following HTML:

```md
;-->includepy<-- tests/example.py
;-->pyobject<-- factorial
```

You can use any number of semi-colons.
For example, to show how to escape a `includepy` block you can write the following Markdown:

```md
;;;-->includepy<-- tests/example.py
;;;-->pyobject<-- factorial
```

You will get the following HTML:

```md
;;-->includepy<-- tests/example.py
;;-->pyobject<-- factorial
```
