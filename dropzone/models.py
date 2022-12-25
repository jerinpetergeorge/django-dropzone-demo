from pathlib import Path

from django.db import models

from .conf import settings as dz_settings
from .utils import sizeof_fmt


class Session(models.Model):
    uuid = models.UUIDField(unique=True)
    total_size = models.IntegerField()
    total_chunks = models.IntegerField()
    chunk_size = models.IntegerField()
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.uuid)

    @property
    def humanized_total_size(self):
        return sizeof_fmt(self.total_size)

    @property
    def humanized_chunk_size(self):
        return sizeof_fmt(self.chunk_size)

    def create_chunk(self, file, index, **kwargs):
        return ChunkedFile.objects.create(
            session=self,
            file=file,
            index=index,
        )

    @property
    def is_complete(self):
        return self.chunks.count() == self.total_chunks

    def merge_chunks(self, **kwargs):
        if not self.is_complete:
            raise ValueError("Chunks are not complete")

        Path(dz_settings.FILE_PROCESSING_DIR).mkdir(
            # create the directory if it doesn't exist
            exist_ok=True,
            parents=True,
        )

        # Since we are using the UUID to create the file name, we can be
        # sure that the file name is unique and thus appending to this
        # newly created file will give us the merged file.
        file_path = dz_settings.FILE_PROCESSING_DIR / f"{self.uuid}-{self.file_name}"
        file_stream = open(file_path, "ab")

        for chunk in self.chunks.order_by("index"):
            file_stream.write(chunk.file.read())


class ChunkedFile(models.Model):
    SEP = "___"

    def chunk_upload_path(self, filename):
        return (
            f"{dz_settings.FILE_UPLOAD_DIR}/{self.session.uuid}"
            f"/{self.index}{self.SEP}{filename}"
        )

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="chunks",
        related_query_name="chunk",
    )
    file = models.FileField(upload_to=chunk_upload_path)
    index = models.IntegerField(db_index=True)

    def __str__(self):
        return str(self.session)
