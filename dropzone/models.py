from django.db import models

from .utils import sizeof_fmt


class Session(models.Model):
    uuid = models.UUIDField(unique=True)
    total_size = models.IntegerField()
    total_chunks = models.IntegerField()
    chunk_size = models.IntegerField()

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
        for chunk in self.chunks.all():
            # do some magic here
            pass


class ChunkedFile(models.Model):
    SEP = "___"

    def chunk_upload_path(self, filename):
        return f"dropzone/{self.session.uuid}/{self.index}{self.SEP}{filename}"

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
