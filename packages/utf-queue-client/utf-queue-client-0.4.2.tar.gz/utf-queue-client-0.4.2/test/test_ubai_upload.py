from utf_queue_client.scripts.ubai_upload_cli import cli, cli_entrypoint
import os


def test_ubai_upload_cli():
    file = os.path.join(os.path.dirname(__file__), "test.hex")
    metadata = [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
    ]

    username = os.environ["UTF_QUEUE_CLIENT_USERNAME"]
    password = os.environ["UTF_QUEUE_CLIENT_PASSWORD"]
    client_id = "utf_queue_client_unittest"
    cli(file, metadata, username, password, client_id)

def test_ubai_upload_cli_script():
    file = os.path.join(os.path.dirname(__file__), "test.hex")
    metadata = [
        ("app_name", "ubai_unit_test"),
        ("branch", "master"),
        ("stack", "ble"),
        ("build_number", "b140"),
        ("target", "brd4180b"),
    ]

    client_id = "utf_queue_client_unittest"
    cli(file, metadata, username, password, client_id)