from rest_framework import serializers

from order_control.models import Purchase, PurchasedItems


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class PurchasedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedItems
        fields = '__all__'


