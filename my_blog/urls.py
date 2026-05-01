"""
URL configuration for my_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from magazine.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' ,signup,name="signup"),
    path('log_in/' ,log_in,name="login"),
    path('home/',home,name='home'),
    path('logout/', log_out, name="logout"),
    path('create/',create_magazine, name='create_magazine'),
    path('edit/<slug:slug>/',edit_magazine,name="edit_magazine"),
    path('delete/<slug:slug>/', delete_magazine, name='delete_magazine'),
    path('profile/<str:username>/',profile,name='profile'),
    path('<slug:slug>/',magazine_detail,name='magazine_detail'),   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
