---
icon: lucide/list
---

# Options

## For `includepy` blocks

- `pyobject`: the name of the Python object; **required**.

- `lines_before`: the number of lines before `pyobject` to include; **default:** 0.

- `lines_after`: the number of lines after `pyobject` to include; **default:** 0.

- `extra_indent`: the number of additional spaces to indent each line; **default:** 0.

- `only_lines`: a comma-separated string of line numbers and/or line ranges (``m-n``, ``m-``, ``-n``, ``n``).

## Extension priority

By default, `includepy` registers itself with a priority of 100, so that it can process the input text before the [pymdownx.superfences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/) preprocessors, which have priorities of 25 (`SuperFencesBlockPreprocessor`) and 80 (`SuperFencesCodeBlockProcessor`).

If this priority causes issues with other extensions, you can specify a different priority in your configuration file:

=== "`zensical.toml`"

    ```toml
    [project.markdown_extensions.includepy]
    priority = 100
    ```

=== "`mkdocs.yml`"

    ```yaml
    markdown_extensions:
      - includepy:
          priority: 100
    ```
