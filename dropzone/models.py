from tempfile import NamedTemporaryFile

from django.core.files.storage import default_storage
from django.db import models

from .conf import settings as dz_settings
from .exceptions import DZFileMergeError, DZFileNotFoundError
from .utils import sizeof_fmt


class Session(models.Model):
    def session_upload_path(self, filename, dir_path=None):
        if dir_path is None:
            dir_path = dz_settings.FILE_UPLOAD_SESSION_DIR

        return f"{dir_path}/{self.uuid}--{filename}"

    uuid = models.UUIDField(unique=True)
    total_size = models.IntegerField()
    total_chunks = models.IntegerField()
    chunk_size = models.IntegerField()
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=session_upload_path, blank=True, null=True)

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

    def safe_delete_chunks(self):
        if not self.file:
            msg = (
                f"Unable to find the merged file associated "
                f"with this session ({self.uuid})"
            )
            raise DZFileNotFoundError(msg)

        for chunk in self.chunks.all():
            chunk.file.delete()
            chunk.delete()

    def merge_chunks(self, **kwargs):
        if not self.is_complete:
            msg = "Unable to merge chunks because the session is not complete"
            raise DZFileMergeError(msg)

        # Create a temporary file to merge the chunks into
        temp_file = NamedTemporaryFile(mode="ab+", delete=True, prefix="dz-temp-")

        # Merge the chunks into the temporary file
        for chunk in self.chunks.order_by("index"):
            temp_file.write(chunk.file.read())

        # Set pointer to the beginning of the file
        temp_file.seek(0)

        # Create a new file in the storage backend
        file_path = self.session_upload_path(self.file_name)
        file = default_storage.save(file_path, temp_file)

        self.file = file
        self.save(update_fields=["file"])

        # Delete the temporary file
        temp_file.close()

        # Delete the chunks
        self.safe_delete_chunks()


class ChunkedFile(models.Model):
    SEP = "___"

    def chunk_upload_path(self, filename):
        return (
            f"{dz_settings.FILE_UPLOAD_CHUNKS_DIR}/{self.session.uuid}"
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
