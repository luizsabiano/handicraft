"""handicraft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from order_control import views

# api <--
from rest_framework import routers
from order_control.api import PurchaseViewSet, PurchasedItemsViewSet

# desativa a necessidade de barra no fim do endereço
#router = routers.DefaultRouter(trailing_slash=False)

router = routers.DefaultRouter()
router.register(r'purchases', PurchaseViewSet)
router.register(r'purchasesItems', PurchasedItemsViewSet)

# api -->

app_name = 'order_control'

urlpatterns = [
    url(r'^api/', include(router.urls)),

    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.HomeView.as_view(), name='homeView'),
    path('client/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:id>/destroy/', views.client_destroy, name='client_destroy'),
    path('clients/<int:id>/detail/', views.client_details, name='client_detail'),

    path('order/', views.order_create, name='order_create'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order_add_items/', views.order_add_items, name='order_add_items'),
    path('orders/<int:id>/update/', views.order_update, name='order_update'),
    path('orders/<int:id>/payment/', views.order_payment, name='order_payment'),
    path('orders/<int:id>/payment_destroy/', views.payment_destroy, name='payment_destroy'),
    path('orders/<int:id>/destroy/', views.order_destroy, name='order_destroy'),
    path('orders/<int:id>/detail/', views.order_details, name='order_detail'),
    path('orders/<int:id>/order_items_details/', views.order_items_details, name='order_items_details'),

    path('orders/<int:id>/loyatyCard_details/', views.loyatyCard_details, name='loyatyCard_details'),

    path('orders/items/<int:id>/destroy/', views.order_items_destroy, name='order_items_destroy'),
    path('orders/items/<int:id>/update/', views.order_items_update, name='order_items_update'),
    path('orders/<int:id>/loyatyCard_details/update/', views.loyatyCard_update, name='loyatyCard_update'),
    path('purchases/', views.PurchaseView.as_view(), name='purchase_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
