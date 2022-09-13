from rest_framework import serializers
from .models import Item, Import


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['type', 'id', 'parentId']


class ImportSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta:
        model = Import
        fields = ['update_date']

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        update_date = Import.objects.create(**'update_date')
        for item in items_data:
            Item.objects.create(**item)
        return update_date


