import os

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv(".env")

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "task-files"

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

container_client = blob_service_client.get_container_client(
    container_name
)


def upload_file(file):
    if not file or not file.filename:
        return None

    blob_client = container_client.get_blob_client(file.filename)

    blob_client.upload_blob(
        file,
        overwrite=True
    )

    return file.filename
