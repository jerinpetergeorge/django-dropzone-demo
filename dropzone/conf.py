from conf import AppSettings

ONE_MB = 1000000

IMPORT_DROPZONE_CONFIG = []
MERGE_DICT_CONFIG = ["JS_OPTIONS"]

FILE_FIELD_NAME = "file"
BASE_DIR_NAME = "dropzone"

DZ_UPLOAD_DIR = f"{BASE_DIR_NAME}/uploads"  # dir relative to MEDIA_ROOT"
DEFAULT_DROPZONE_CONFIG = {
    "JS_OPTIONS": {
        "url": "/upload/",
        "method": "post",
        "chunking": True,
        "forceChunking": False,
        "chunkSize": ONE_MB * 2,  # 2MB
        "retryChunks": True,
        "retryChunksLimit": 3,
        "maxFilesize": None,
        "paramName": FILE_FIELD_NAME,
        "maxFiles": 10,
        "acceptedFiles": None,
    },
    "FILE_UPLOAD_DIR": DZ_UPLOAD_DIR,  # /media/dropzone/uploads
    # /media/dropzone/uploads/chunks
    "FILE_UPLOAD_CHUNKS_DIR": f"{DZ_UPLOAD_DIR}/chunks",
    # /media/dropzone/uploads/session
    "FILE_UPLOAD_SESSION_DIR": f"{DZ_UPLOAD_DIR}/session",
    "FILE_FIELD_NAME": FILE_FIELD_NAME,
}

settings = AppSettings(
    "DROPZONE_CONFIG",
    DEFAULT_DROPZONE_CONFIG,
    IMPORT_DROPZONE_CONFIG,
    MERGE_DICT_CONFIG,
)
