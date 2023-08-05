import os

from utf_queue_client.clients.ubai_artifact_upload_request_producer import (
    UbaiArtifactUploadRequestProducer,
)
from urllib import parse
import click
from typing import Iterable, Tuple


@click.command()
@click.option(
    "--file-path",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to file to upload",
)
@click.option("--metadata", multiple=True, type=(str, str))
@click.option(
    "--username",
    envvar='UTF_QUEUE_USERNAME',
    help="UTF queue username",
)
@click.option(
    "--password",
    envvar='UTF_QUEUE_PASSWORD',
    help="UTF queue password",
)
@click.option(
    "--client-id", type=str, default="Unknown Client", help="Optional client identifier"
)
def cli_entrypoint(
    file_path: str,
    metadata: Iterable[Tuple[str, str]],
    username: str,
    password: str,
    client_id: str,
):
    cli(file_path, metadata, username, password, client_id)


def cli(
    file_path: str,
    metadata: Iterable[Tuple[str, str]],
    username: str,
    password: str,
    client_id: str,
):
    hostname = os.environ.get("UTF_QUEUE_HOSTNAME", "utf-queue-central.silabs.net")

    url = f"amqps://{username}:{parse.quote(password)}@{hostname}:443"

    client = UbaiArtifactUploadRequestProducer(url, client_id)
    metadata_dict = {}
    for key, value in metadata:
        metadata_dict[key] = value
    client.upload_artifact(file_path, metadata=metadata_dict)
