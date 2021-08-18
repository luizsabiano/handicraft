from rest_framework import serializers, pagination

from order_control.models import Purchase, PurchasedItems


class PurchasedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItems
        fields = ('id', 'name', 'amount', 'quantity')


class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchasedItemsSerializer(many=True, read_only=False)

    class Meta:
        model = Purchase
        fields = ['id', 'createAt', 'amount', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)
        for item_data in items_data:
            PurchasedItems.objects.create(purchase=purchase, **item_data)
        return purchase
