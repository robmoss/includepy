from pathlib import Path
import pytest
from includepy import IncludePyProc


def locate_examples():
    """
    Locate each example input file.
    """
    examples_dir = Path("./examples")
    example_files = list(examples_dir.glob("*.in"))
    return [f.stem for f in example_files]


@pytest.mark.parametrize("example_name", locate_examples())
def test_example(example_name):
    """
    Check that we obtained the expected (Markdown) output for an example.
    """
    input_file = Path("./examples") / f"{example_name}.in"
    output_file = Path("./examples") / f"{example_name}.out"

    with open(output_file) as f:
        expected_text = f.read()

    expected_lines = expected_text.split("\n")

    with open(input_file) as f:
        input_text = f.read()

    input_lines = input_text.split("\n")
    processor = IncludePyProc(config={}, md=None)
    output_lines = processor.run(input_lines)

    assert output_lines == expected_lines
