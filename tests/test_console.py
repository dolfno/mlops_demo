import click.testing
import pytest

from fake_data import FakeDataLoader

from python_ci_template import console


# Init cache
FakeDataLoader(
    "./fixtures/cassette.pkl",
    console.get_tags,
    **{"glue_connection": "nldevun_a17a_ro"}
).data


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_get_tags(mocker):
    mock = mocker.patch("python_ci_template.console.get_tags")
    f = FakeDataLoader(
        "./fixtures/cassette.pkl",
        console.get_tags,
        **{"glue_connection": "nldevun_a17a_ro"}
    )
    mock.return_value = f.data
    return mock


def test_main_invokes_get_tags(runner, mock_get_tags):
    runner.invoke(console.main)
    assert mock_get_tags.called


def test_main_print_title(runner, mock_get_tags):
    results = runner.invoke(console.main)
    assert "ciqSQaQhmoiKB7ccPjXXrU" in results.output


def test_main_uses_glue_conn(runner, mock_get_tags):
    runner.invoke(console.main)
    args, _ = mock_get_tags.call_args
    assert "nldevun_a17a_ro" in args[0]


def test_main_fails_on_get_tags_error(runner, mock_get_tags):
    mock_get_tags.side_effect = Exception("Cache isnt there")
    result = runner.invoke(console.main)
    assert result.exit_code == 1
