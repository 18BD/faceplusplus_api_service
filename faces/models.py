from django.db import models


class Face(models.Model):
    image_id = models.CharField(max_length=100)
    face_tokens = models.JSONField()
    image_file = models.ImageField(upload_to='faces/', )