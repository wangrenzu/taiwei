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
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.HomeAPIView.as_view()),
    path("update/", views.UpdateOrder.as_view()),
    path("updateUser/", views.UpdateUser.as_view()),
    path("updateGoods/", views.UpdateGoods.as_view()),
    path("updateMaterials/", views.UpdateMaterials.as_view()),
    path("updateCommodity/", views.UpdateCommodity.as_view()),
    path("updateOneCommodity/", views.UpdateOneCommodity.as_view()),
    path("updateStock/", views.UpdateStock.as_view()),
    path("updateStockIn/", views.UpdateStockIn.as_view()),
    path("updateSalesRecord/", views.UpdateSalesRecord.as_view()),
    path("updateSize/", views.UpdateSize.as_view()),
    path("all/", views.HomeAllView.as_view()),
    path("summary/", views.SummaryView.as_view()),
    path("userAll/", views.UserAll.as_view()),
    path("getReportList/", views.getReportList.as_view()),
    path("userInfo/", views.getUserInfo.as_view()),
    path("updateStatus/", views.UpdateStatusView.as_view()),
    path("updateRepeatOrder/", views.updateRepeatOrder.as_view()),
    path("updateFabric/", views.updateFabric.as_view()),
    path("updateFactory/", views.updateFactory.as_view()),
    path("vipUser/", views.VipUserView.as_view()),
    re_path(r"^codeInfo/(?P<submit_time>.*)/$", views.getCodeInfo.as_view()),
    path('orderTracking/', views.OrderTrackingView.as_view()),
    path('searchCode/', views.SearchCodeView.as_view()),
    path('StyleStatusView/', views.StyleStatusView.as_view()),
]
