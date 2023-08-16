"""clothing URL Configuration

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

from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('roomInfo/', views.RoomView.as_view()),
    path('Integration/', views.IntegrationView.as_view()),
    path('Barrage/', views.Barrage.as_view()),
    path('productInfo/', views.ProductInfoView.as_view()),
    path("LiveRoomData/", views.LiveRoomDataView.as_view()),
    path("echarts1/", views.echarts1),
    path("echarts2/", views.echarts2),
    path("echarts3/", views.echarts3),
    path("echarts4/", views.echarts4),
    path("updatecode/", views.update_code),
    path("getcode/", views.get_code),
]
