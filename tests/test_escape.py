import markdown
import textwrap
from includepy import IncludePy


def test_escape_simple():
    """
    Verify that IncludePy directives can be escaped.
    """
    text = textwrap.dedent(
        """
        ```
        ;-->includepy<-- tests/example.py
        ;-->some_option<-- some_value
        ;;-->includepy<-- tests/example.py
        ;;-->some_option<-- some_value
        ;;;-->includepy<-- tests/example.py
        ;;;-->some_option<-- some_value
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>;--&gt;includepy&lt;-- tests/example.py
        ;--&gt;some_option&lt;-- some_value
        ;;--&gt;includepy&lt;-- tests/example.py
        ;;--&gt;some_option&lt;-- some_value
        ;;;--&gt;includepy&lt;-- tests/example.py
        ;;;--&gt;some_option&lt;-- some_value
        </code></pre>"""
    )
    assert original_html == expected_original

    includepy_html = markdown.markdown(
        text, extensions=[IncludePy(), "fenced_code"]
    )
    assert original_html != includepy_html

    # NOTE: The slash after the opening triple-quotes prevents an empty first
    # line.
    expected_html = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;some_option&lt;-- some_value
        ;--&gt;includepy&lt;-- tests/example.py
        ;--&gt;some_option&lt;-- some_value
        ;;--&gt;includepy&lt;-- tests/example.py
        ;;--&gt;some_option&lt;-- some_value
        </code></pre>"""
    )

    assert includepy_html == expected_html
