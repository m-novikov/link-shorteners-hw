from django.db import models


class Link(models.Model):
    # Если использовать ПГ то лучше использовать hash index, так как нам важны только = операции
    link_hash = models.CharField(max_length=6, unique=True, null=False)
    url = models.URLField(unique=True, null=False)
    creation_date = models.DateTimeField("Date created", auto_now_add=True)
    hits = models.PositiveIntegerField("Hit count", default=0)