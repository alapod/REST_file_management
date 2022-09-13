from django.db import models
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel, TreeForeignKey


class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.CharField(null=True, max_length=255)
    date = models.DateTimeField(null=True)
    parentId = models.CharField(null=True, max_length=255)#TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    type = models.CharField(default=('FOLDER', 'FILE'), max_length=6)
    size = models.IntegerField(null=True, validators=[MinValueValidator])
    parent = models.CharField(null=True, max_length=255)

class Import(models.Model):
    update_date = models.DateTimeField()








