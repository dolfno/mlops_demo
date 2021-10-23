import nox
from nox import Session

locations = "src", "noxfile.py"
nox.options.sessions = "lint", "tests"


@nox.session(python="3.9")
def tests(session: Session) -> None:
    session.run("poetry", "install", external=True)
    session.run("pytest", "--cov")


@nox.session(python="3.9")
def lint(session: Session) -> None:
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
    )
    args = session.posargs or locations
    session.run("flake8", *args)


@nox.session(python="3.9")
def black(session: Session) -> None:
    session.install("black")
    args = session.posargs or locations
    session.run("black", *args, "--line-length=120")


@nox.session(python="3.9")
def pytype(session: Session) -> None:
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.install("pytype")
    session.run("pytype", *args)


package = "hypermodern_python"


@nox.session(python=["3.9"])
def typeguard(session: Session) -> None:
    args = session.posargs or ["-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    session.install("pytest", "pytest-mock", "typeguard")
    session.run("pytest", f"--typeguard-packages={package}", *args)
