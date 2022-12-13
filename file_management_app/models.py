from django.db import models
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.utils import timezone


class Item(MPTTModel):
    id = models.CharField(primary_key=True, max_length=255)
    url = models.CharField(null=True, max_length=255)
    parentId = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    type = models.CharField(default=("FOLDER", "FILE"), max_length=6)
    size = models.PositiveIntegerField(null=True, default=0)
    update_date = models.DateTimeField(default=timezone.now)

    class MPTTMeta:
        order_insertion_by = []
        parent_attr = "parentId"
