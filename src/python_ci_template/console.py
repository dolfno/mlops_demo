import click
import awswrangler as wr
import boto3
from . import __version__


def get_tags(glue_connection):
    con = wr.mysql.connect(glue_connection)
    con.select_db("cb_data")
    return wr.mysql.read_sql_query("select uuid, name from tags limit 1", con)


@click.command()
@click.option(
    "--glue_connection",
    "-gl",
    default="nldevun_a17a_ro",
    help="Glue connection name for awswrangler",
    metavar="GLUE",
    show_default=True,
)
@click.option(
    "--aws_region",
    "-ar",
    default="eu-west-1",
    help="AWS default region for boto connection",
    metavar="AWSR",
    show_default=True,
)
@click.version_option(version=__version__)
def main(glue_connection: str, aws_region: str) -> None:
    """The hypermodern Python project."""
    boto3.setup_default_session(region_name=aws_region)

    click.echo(click.style('Hello there', bg='blue', fg='white'))
    click.echo('glue con is now {}'.format(glue_connection))
    tags = get_tags(glue_connection)
    click.echo("found some tags {}".format(tags.to_string()))
