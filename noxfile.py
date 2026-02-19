import nox


@nox.session(default=False)
def build(session):
    """Build source and binary (wheel) packages."""
    session.install("build")
    session.run("python", "-m", "build")


@nox.session()
def tests(session):
    """Run test cases and record test coverage."""
    session.install(".[tests]")
    package = "includepy"
    session.run(
        "pytest",
        f"--cov={package}",
        "--pyargs",
        package,
        "./tests",
        *session.posargs,
    )


@nox.session()
def docs(session):
    """Build the documentation."""
    session.install(".[docs]")
    if session.posargs:
        session.run("zensical", *session.posargs)
    else:
        session.run("zensical", "build")


@nox.session()
def ruff(session):
    """Check code for linter warnings and formatting issues."""
    # check_files = ["src", "tests", "doc", "noxfile.py"]
    check_files = ["src", "tests", "noxfile.py"]
    session.install("ruff >= 0.15")
    session.run("ruff", "check", *check_files)
    session.run("ruff", "format", "--diff", *check_files)


@nox.session()
def mypy(session):
    """Check code for type issues."""
    session.install("mypy >= 1.19", "types-markdown")
    session.run("mypy", "src")
