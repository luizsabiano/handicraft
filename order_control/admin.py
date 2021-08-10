from django.contrib import admin

from order_control.models import Client, Order, BoxTop, LoyatyCard, Adhesive, Payment, Purchase, PurchasedItems

admin.site.register(Client)
admin.site.register(Order)
admin.site.register(BoxTop)
admin.site.register(LoyatyCard)
admin.site.register(Adhesive)
admin.site.register(Payment)
admin.site.register(Purchase)
admin.site.register(PurchasedItems)

