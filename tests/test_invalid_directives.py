import markdown
import pytest
import textwrap
from includepy import IncludePy, IncludePyError


def test_no_pyobject():
    """
    Verify that an exception is raised if there is no "pyobject" line.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        </code></pre>"""
    )
    assert original_html == expected_original

    with pytest.raises(IncludePyError, match="No Python object specified"):
        markdown.markdown(text, extensions=[IncludePy(), "fenced_code"])


def test_invalid_option():
    """
    Verify that invalid options raise an exception.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        -->pyobject<-- factorial
        -->unknown_option<-- value
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- factorial
        --&gt;unknown_option&lt;-- value
        </code></pre>"""
    )
    assert original_html == expected_original

    with pytest.raises(IncludePyError, match="Invalid option unknown_option"):
        markdown.markdown(text, extensions=[IncludePy(), "fenced_code"])


def test_duplicate_option():
    """
    Verify that duplicate options raise an exception.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        -->pyobject<-- factorial
        -->pyobject<-- factorial
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- factorial
        --&gt;pyobject&lt;-- factorial
        </code></pre>"""
    )
    assert original_html == expected_original

    with pytest.raises(IncludePyError, match="Duplicate option pyobject"):
        markdown.markdown(text, extensions=[IncludePy(), "fenced_code"])


def test_missing_objects():
    """
    Verify that missing objects raise an exception.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        -->pyobject<-- notdefined
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- notdefined
        </code></pre>"""
    )
    assert original_html == expected_original

    with pytest.raises(
        IncludePyError, match="Found 0 matches for notdefined"
    ):
        markdown.markdown(text, extensions=[IncludePy(), "fenced_code"])


def test_duplicate_objects():
    """
    Verify that duplicate objects with the same name raise an exception.
    """
    text = textwrap.dedent(
        """
        ```
        -->includepy<-- tests/example.py
        -->pyobject<-- duplicated
        ```
        """
    )

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    expected_original = textwrap.dedent(
        """\
        <pre><code>--&gt;includepy&lt;-- tests/example.py
        --&gt;pyobject&lt;-- duplicated
        </code></pre>"""
    )
    assert original_html == expected_original

    with pytest.raises(
        IncludePyError, match="Found 2 matches for duplicated"
    ):
        markdown.markdown(text, extensions=[IncludePy(), "fenced_code"])
