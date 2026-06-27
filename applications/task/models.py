from django.db import models


class Task(models.Model):
    song_name = models.CharField(max_length=255, default="")
    artist_name = models.CharField(max_length=255, default="")

    full_path = models.CharField(max_length=255)
    state = models.CharField(max_length=255, default="wait")
    parent_path = models.CharField(max_length=255, default="")
    filename = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(null=True, auto_now_add=True)


class TaskRecord(models.Model):
    song_name = models.CharField(max_length=255, default="")
    artist_name = models.CharField(max_length=255, default="")
    full_path = models.CharField(max_length=255, default="")
    tag_source = models.CharField(max_length=255, default="")
    icon = models.CharField(max_length=255, default="icon-folder")
    state = models.CharField(max_length=255, default="wait")
    extra = models.TextField(default="")
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    batch = models.CharField(max_length=255, default="")


class BatchTask(models.Model):
    batch_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=32, default="running")  # running / done
    total = models.IntegerField(default=0)
    success = models.IntegerField(default=0)
    failed = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
