from rest_framework import viewsets, status
from rest_framework.response import Response

from order_control.models import Purchase, PurchasedItems
from order_control.serializers import PurchaseSerializer, PurchasedItemsSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        dados = request.data
        dataDict = {}
        dataList = []
        purchaseSerializer = PurchaseSerializer(data=dados['purchases'])

        if purchaseSerializer.is_valid():
            purchase = purchaseSerializer.save()
            pid = purchase.id
            dataDict['purchases'] = purchaseSerializer.data

            for dado in dados['items']:
                dados['items'][dado]['purchase'] = pid
                dado = PurchasedItemsSerializer(data=dados['items'][dado])

                if dado.is_valid():
                    dado.save()
                    dataList.append(dado.data)

            dataDict['items'] = dataList

            data = dataDict
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(purchaseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchasedItemsViewSet(viewsets.ModelViewSet):
    serializer_class = PurchasedItemsSerializer
    queryset = PurchasedItems.objects.all()
