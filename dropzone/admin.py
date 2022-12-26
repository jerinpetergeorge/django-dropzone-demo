from django.contrib import admin

from .models import ChunkedFile, Session


class ChunkedFileInline(admin.TabularInline):
    model = ChunkedFile
    extra = 0
    fields = ("index", "file")
    readonly_fields = ("index", "file")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "humanized_total_size",
        "total_chunks",
        "humanized_chunk_size",
        "is_complete",
    )
    inlines = (ChunkedFileInline,)
    readonly_fields = (
        "uuid",
        "humanized_total_size",
        "total_chunks",
        "humanized_chunk_size",
        "is_complete",
        "file",
    )
    fields = readonly_fields
