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
    path('', views.DesignView.as_view()),
    path('tags/', views.TagsView.as_view()),
    path('size/', views.SizeView.as_view()),
    path('script/', views.ScriptView.as_view()),
    path('collocation/', views.CollocationView.as_view()),
    re_path(r'^checkCode/(?P<code>\w.*)/$', views.check_code),
    path('reply/', views.reply),
    path('context_reply/', views.context_reply),
    path('designDetail/', views.DesignDetailView.as_view()),
]
