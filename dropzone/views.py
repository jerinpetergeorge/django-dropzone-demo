import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View, generic

ONE_MB = 1000000


class DropzoneRenderView(generic.TemplateView):
    template_name = "dropzone/upload.html"
    upload_path = reverse_lazy("dropzone:upload")

    def get_dropzone_config(self, **kwargs) -> dict:
        return {
            "url": str(self.upload_path),
            "method": "post",
            "chunking": True,
            "forceChunking": True,
            "chunkSize": ONE_MB * 2,  # 2MB
            "retryChunks": True,
            "retryChunksLimit": 3,
            "maxFilesize": None,
            "paramName": "file",
            "maxFiles": 10,
            "acceptedFiles": None,
        }

    def get_context_data(self, **kwargs):
        kwargs["dropzone_config"] = json.dumps(self.get_dropzone_config(**kwargs))
        return super().get_context_data(**kwargs)


class DropzoneUploadView(generic.View):
    file_param = "file"

    def post(self, request, *args, **kwargs):
        file = request.FILES.get(self.file_param)
        return JsonResponse({"success": True})
