from dataclasses import dataclass
from typing import List

import awswrangler as wr
import boto3
import click
import desert
from pymysql.cursors import DictCursor

from . import __version__


@dataclass
class Tag:
    name: str
    uuid: str

    def __str__(self) -> str:
        return f"Tag {self.name} with uuid {self.uuid}"


tag_schema = desert.schema(Tag)


def get_tags(glue_connection: str) -> List[Tag]:
    tags = []
    con = wr.mysql.connect(glue_connection)
    con.select_db("cb_data")
    with con.cursor(DictCursor) as cursor:
        cursor.execute("select uuid, name from tags limit 2")
        for row in cursor:
            tags.append(tag_schema.load(row))
    con.close()
    return tags


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

    click.echo(click.style("Hello there", bg="blue", fg="white"))
    click.echo("glue con is now {}".format(glue_connection))
    tags = get_tags(glue_connection)
    if tags:
        click.echo("found some tags {}".format(tags[0]))
