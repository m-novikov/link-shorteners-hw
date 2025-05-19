from django.db import models
from django.core.validators import MinLengthValidator


class Link(models.Model):
    # Если использовать ПГ то лучше использовать hash index, так как нам важны только = операции
    link_hash = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6)])
    url = models.URLField(unique=True, null=False)
    creation_date = models.DateTimeField("Date created", auto_now_add=True)
    hits = models.PositiveIntegerField("Hit count", default=0)


class LinkHit(models.Model):
    creation_date = models.DateTimeField("Date created", auto_now_add=True, db_index=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='link_hits')

    class Meta:
        ordering = ['-creation_date']