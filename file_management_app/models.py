from django.db import models
from django.core.validators import MinValueValidator
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.utils import timezone


class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.CharField(null=True, max_length=255)
    parentId = models.CharField(null=True, max_length=255)
    type = models.CharField(default=('FOLDER', 'FILE'), max_length=6)
    size = models.IntegerField(null=True, validators=[MinValueValidator])
    update_date = models.DateTimeField(default=timezone.now)


class Relations(models.Model):
    parent = models.ForeignKey(Item, max_length=255, null=True, on_delete=models.CASCADE)
    child = models.CharField(null=True, max_length=255)


"""
class Item(MPTTModel):
  id = models.CharField(primary_key=True, max_length=255)
  url = models.CharField(null=True, max_length=255)
#  parentId = models.CharField(null=True, max_length=255)
  parentId = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
  #parentId = models.CharField(max_length=255, null=True)
  type = models.CharField(default=('FOLDER', 'FILE'), max_length=6)
  size = models.IntegerField(null=True, validators=[MinValueValidator])
  update_date = models.DateTimeField(default=timezone.now)
  #children = models.CharField(max_length=255)

  class MPTTMeta:
      order_insertion_by = []
      parent_attr = 'parentId'
      """

"""class Relations(models.Model):
    parentId = models.CharField(primary_key=True, max_length=255)
    childId = models.CharField(primary_key=True, null=True, max_length=255)
"""


