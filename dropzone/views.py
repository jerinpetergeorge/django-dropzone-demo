import json
from functools import cached_property
from uuid import uuid4

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .conf import settings as dz_settings
from .models import Session


class UploadAttrMixin:
    upload_path: str

    def get_upload_path(self):
        return self.upload_path

    @cached_property
    def upload_path_url(self):
        return str(self.get_upload_path())


class DropzoneRenderMixin:
    template_name = "dropzone/upload.html"

    def get_dropzone_config(self, **kwargs) -> dict:
        return {**dz_settings.JS_OPTIONS, **kwargs}

    def get_context_data(self, **kwargs):
        kwargs["dropzone_config"] = json.dumps(self.get_dropzone_config(**kwargs))
        return super().get_context_data(**kwargs)


class DropzoneAbstractRenderView(
    DropzoneRenderMixin,
    UploadAttrMixin,
    generic.TemplateView,
):
    ...


class DropzoneNonChunkedUploadView(DropzoneAbstractRenderView):
    def get_dropzone_config(self, **kwargs) -> dict:
        kwargs = super().get_dropzone_config(chunking=False, **kwargs)
        return kwargs


class DropzoneChunkedUploadView(DropzoneAbstractRenderView):
    chunk_size = dz_settings.JS_OPTIONS["chunkSize"]
    retry_chunks = dz_settings.JS_OPTIONS["retryChunks"]
    retry_chunks_limit = dz_settings.JS_OPTIONS["retryChunksLimit"]

    def get_dropzone_config(self, **kwargs) -> dict:
        _conf = {
            "chunking": True,
            "chunkSize": self.chunk_size,
            "retryChunks": self.retry_chunks,
            "retryChunksLimit": self.retry_chunks_limit,
            "mergeURL": reverse("dropzone:merge"),
        }
        kwargs.update(_conf)
        return super().get_dropzone_config(**kwargs)


class DropzoneRenderView(DropzoneChunkedUploadView):
    upload_path = reverse_lazy("dropzone:upload")


class DropzoneUploadAbstractView(generic.View):
    file_param = dz_settings.FILE_FIELD_NAME

    def _process_normal_upload(self, file, *args, **kwargs):
        ...

    def _process_chunked_upload(self, file, *args, **kwargs):
        ...

    def process_file(self, file, *args, **kwargs):
        payload = self.request.POST
        if "dzuuid" not in payload:
            # When the size of the upload file below the
            # chunk size, it won't include certain fields.
            #
            # So we can assume that it's a normal upload and
            # need to set it on `Session` model.
            return self._process_normal_upload(file, *args, **kwargs)

        return self._process_chunked_upload(file, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get(self.file_param)
        self.process_file(file=file)
        return JsonResponse({"success": True})


class DropzoneUploadView(DropzoneUploadAbstractView):
    def create_session(self, file, *args, **kwargs):
        return Session.objects.create(
            file_name=file.name,
            total_size=file.size,
            total_chunks=1,
            chunk_size=file.size,
            file=file,
            **kwargs,
        )

    def get_or_create_session(
        self,
        uuid,
        total_size,
        total_chunks,
        chunk_size,
        file_name,
    ):
        session, created = Session.objects.get_or_create(
            uuid=uuid,
            defaults={
                "total_size": total_size,
                "total_chunks": total_chunks,
                "chunk_size": chunk_size,
                "file_name": file_name,
            },
        )
        return session

    def _process_normal_upload(self, file, *args, **kwargs):
        return self.create_session(file, uuid=uuid4())

    def _process_chunked_upload(self, file, *args, **kwargs):
        payload = self.request.POST
        uuid = payload["dzuuid"]
        chunk_index = payload["dzchunkindex"]
        total_size = payload["dztotalfilesize"]
        chunk_size = payload["dzchunksize"]
        total_chunks = payload["dztotalchunkcount"]
        file_name = self.request.FILES[self.file_param].name
        session = self.get_or_create_session(
            uuid,
            total_size,
            total_chunks,
            chunk_size,
            file_name,
        )
        session.create_chunk(file, index=chunk_index)


class DropzoneMergeView(generic.View):
    def get_or_404(self):
        return get_object_or_404(Session, uuid=self.request.POST.get("dzuuid", ""))

    def post(self, request, *args, **kwargs):
        session = self.get_or_404()
        session.merge_chunks()
        return JsonResponse({"success": True})
