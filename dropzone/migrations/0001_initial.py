# Generated by Django 4.1.1 on 2022-12-26 04:49

from django.db import migrations, models
import django.db.models.deletion
import dropzone.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(unique=True)),
                ('total_size', models.IntegerField()),
                ('total_chunks', models.IntegerField()),
                ('chunk_size', models.IntegerField()),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=dropzone.models.Session.session_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='ChunkedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=dropzone.models.ChunkedFile.chunk_upload_path)),
                ('index', models.IntegerField(db_index=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chunks', related_query_name='chunk', to='dropzone.session')),
            ],
        ),
    ]
