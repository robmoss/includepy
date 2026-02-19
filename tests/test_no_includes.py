import markdown
from includepy import IncludePy


def test_no_includes():
    """
    Verify that IncludePy has no effect if there are no IncludePy directives.
    """
    text = """
    # Heading

    Some text for a paragraph.

    ```sh
    echo "Example code block
    ```
    """

    original_html = markdown.markdown(text, extensions=["fenced_code"])
    includepy_html = markdown.markdown(
        text, extensions=[IncludePy(), "fenced_code"]
    )

    assert original_html == includepy_html
