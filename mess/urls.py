"""
URL configuration for mess project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_view
from account import views as acc_view
from amount import views as amn_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_view.Home, name='home'),
    path('registration/', acc_view.Registration, name='registration'),
    path('dashboard/', core_view.Dashboard, name='dashboard'),
    path('login/', acc_view.Login, name='login'),
    path('logout/', acc_view.Logout, name='logout'),
    path('mill/', include('mill.urls')),
    path('save_mill/', core_view.save_mill, name='save_mill'),
    path('diposits/', amn_view.ShowDiposit, name='diposits'),
    path('add-diposit/', amn_view.AddDiposit, name='adddiposits'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)