import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client


class SupabaseStorage:
    """
    Storage adapter for Supabase Storage.
    """

    def __init__(
        self,
        bucket: str = "tamazight-corpus",
        prefix:str = "",
    ):
        load_dotenv()

        url = os.environ["SUPABASE_URL"]
        key = os.environ["SUPABASE_KEY"]

        self.client = create_client(url, key)
        self.bucket = bucket
        self.prefix = prefix.strip("/")

    def upload_file(
        self,
        local_path: Path,
        remote_path: str,
        content_type: str,
    ):
        """
        Upload one local file to Supabase Storage.
        """

        data = local_path.read_bytes()

        return (
            self.client
            .storage
            .from_(self.bucket)
            .upload(
                self._path(remote_path),
                data,
                {
                    "content-type": content_type,
                    "upsert": "true",
                },
            )
        )

    def download_file(
        self,
        remote_path: str,
        local_path: Path,
    ):
        """
        Download one file from Supabase Storage.
        """

        data = (
            self.client
            .storage
            .from_(self.bucket)
            .download(self._path(remote_path))
        )

        local_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        local_path.write_bytes(data)

    def upload_text(
        self,
        text: str,
        remote_path: str,
    ):
        """
        Upload text content to Supabase Storage.
        """

        data = text.encode("utf-8")

        return (
            self.client
            .storage
            .from_(self.bucket)
            .upload(self._path(
                remote_path),
                data,
                {
                    "content-type": "text/plain; charset=utf-8",
                    "upsert": "true",
                },
            )
        )

    def download_text(
        self,
        remote_path: str,
    ) -> str:
        """
        Download text content from Supabase Storage.
        """

        data = (
            self.client
            .storage
            .from_(self.bucket)
            .download(self._path(remote_path))
        )

        return data.decode("utf-8")

    def _path(self, remote_path: str) -> str:
        """
        Build a path inside the corpus namespace.
        """
        remote_path = remote_path.strip("/")

        if not self.prefix:
            return remote_path

        return f"{self.prefix}/{remote_path}"