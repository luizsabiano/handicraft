import decimal

from rest_framework import viewsets, status, pagination
from rest_framework.response import Response

from handicraft import settings
from order_control.models import Purchase, PurchasedItems
from order_control.serializers import PurchaseSerializer, PurchasedItemsSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def create(self,  request, *args, **kwargs):
        purchaseSerializer = PurchaseSerializer(data=request.data)
        if purchaseSerializer.is_valid():
            purchaseSerializer.save()
            data = purchaseSerializer.data
            headers = self.get_success_headers(purchaseSerializer.data)
            return Response(data, status=status.HTTP_201_CREATED,  headers=headers)
        else:
            return Response(purchaseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def destroy(self, request, *args, **kwargs):

            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)


class PurchasedItemsViewSet(viewsets.ModelViewSet):
    serializer_class = PurchasedItemsSerializer
    queryset = PurchasedItems.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # subtrai o item do total em purchases
        item = PurchasedItems.objects.get(id=serializer.data['id'])
        item.purchase.amount -= decimal.Decimal(serializer.data['amount'])
        item.purchase.save()
        # -------------------------------------
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
