"""MyAwesomeCart URL Configuration

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

# from django.contrib import admin
from django.urls import path,re_path
from shop import views
urlpatterns = [
    path('',views.index,name='ShopHome'),
    path('about/',views.about,name='AboutUS'),
    path('contact/',views.contact,name='ContactUS'),
    path("products/<int:id>",views.productview,name='ProductView'),
    path('search/',views.search,name='Search'),
    path('tracker/',views.tracker,name='TrackingStatus'),
    path('checkout/',views.checkout,name='Checkout'),
    path('payment/<int:id>/',views.payment,name='Payment'),
    re_path(r'^checkoutDirect/(?P<update_id>\d+)/(?P<id>\d+)/(?P<value>\d+(?:\.\d+)?)/$', views.checkoutDirect, name='checkoutDirect'),
    path('success',views.success,name="Success")
]
