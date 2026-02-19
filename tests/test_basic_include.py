import markdown
import textwrap
from includepy import IncludePy, makeExtension


def test_basic_include_single():
    """
    Verify that a IncludePy directive adds the expected lines.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        -->pyobject<-- factorial
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- factorial
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
        <pre><code>def factorial(n: int) -&gt; int:
            value = n  # (1)
            while n &gt; 1:
                n -= 1
                value *= n
            return value
        </code></pre>"""
    )

    assert includepy_html == expected_html


def test_basic_include_single_extra_lines_1():
    """
    Verify that a IncludePy directive adds the expected additional lines.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        -->pyobject<-- factorial
        -->lines_before<-- 4
        -->lines_after<-- 3
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- factorial
        --&gt;lines_before&lt;-- 4
        --&gt;lines_after&lt;-- 3
        </code></pre>"""
    )
    assert original_html == expected_original

    includepy_html = markdown.markdown(
        text, extensions=[IncludePy(), "fenced_code"]
    )
    assert original_html != includepy_html

    # NOTE: The slash after the opening triple-quotes prevents an empty first
    # line.
    # TODO: do we need to indent the lines in order for markdown to parse them
    # correctly?
    expected_html = textwrap.dedent(
        """\
        <pre><code>def hello(name: str) -&gt; None:
            print(f&quot;Hello {name}!&quot;)


        def factorial(n: int) -&gt; int:
            value = n  # (1)
            while n &gt; 1:
                n -= 1
                value *= n
            return value


        def duplicated() -&gt; int:
        </code></pre>"""
    )

    assert includepy_html == expected_html


def test_basic_include_multiple():
    """
    Verify that multiple IncludePy directives add the expected lines.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        -->pyobject<-- factorial
        -->includepy<-- tests/example.py
        -->pyobject<-- hello
        -->includepy<-- tests/example.py
        -->pyobject<-- something
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- factorial
        --&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- hello
        --&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- something
        </code></pre>"""
    )
    assert original_html == expected_original

    includepy_html = markdown.markdown(
        text, extensions=[makeExtension(), "fenced_code"]
    )
    assert original_html != includepy_html

    # NOTE: The slash after the opening triple-quotes prevents an empty first
    # line.
    expected_html = textwrap.dedent(
        """\
        <pre><code>def factorial(n: int) -&gt; int:
            value = n  # (1)
            while n &gt; 1:
                n -= 1
                value *= n
            return value
        def hello(name: str) -&gt; None:
            print(f&quot;Hello {name}!&quot;)
        def something(arg1, arg2):
            return f&quot;{arg1} and {arg2}&quot;
        </code></pre>"""
    )

    assert includepy_html == expected_html
