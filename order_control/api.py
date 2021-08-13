from rest_framework import viewsets, status
from rest_framework.response import Response

from order_control.models import Purchase, PurchasedItems
from order_control.serializers import PurchaseSerializer, PurchasedItemsSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def create(self,  request, *args, **kwargs):

        purchaseSerializer = PurchaseSerializer(data=request.data)
        if purchaseSerializer.is_valid():
            purchaseSerializer.save()
            data = purchaseSerializer.data
            headers = self.get_success_headers(purchaseSerializer.data)
            return Response(data, status=status.HTTP_201_CREATED,  headers=headers)
        else:
            return Response(purchaseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchasedItemsViewSet(viewsets.ModelViewSet):
    serializer_class = PurchasedItemsSerializer
    queryset = PurchasedItems.objects.all()
