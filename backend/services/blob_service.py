from azure.storage.blob import BlobServiceClient
import uuid

class BlobStorage:
    def __init__(self, conn_str: str, container: str):
        self.client = BlobServiceClient.from_connection_string(conn_str)
        self.container = container
        self.container_client = self.client.get_container_client(container)

    def ensure_container(self):
        try:
            self.container_client.create_container()
        except Exception:
            pass

    def upload_file(self, file_bytes: bytes, filename: str) -> str:
        self.ensure_container()
        blob_name = f"{uuid.uuid4()}__{filename}"
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file_bytes, overwrite=True)
        return blob_name
