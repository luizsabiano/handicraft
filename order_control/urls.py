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
from django.conf.urls.static import static
from django.urls import path

from order_control import views

app_name = 'order_control'

urlpatterns = [
    # path('order_control/create/', views.client_create, name='client_create'),
    path('', views.client_create, name='client_create'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/<int:id>/update/', views.client_update, name='client_update'),
    path('clients/<int:id>/destroy/', views.client_destroy, name='client_destroy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
