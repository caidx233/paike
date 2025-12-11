"""
URL configuration for paike project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls import include
from paike import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('choice/', include('choice.urls')),
    path('',views.index,name='index'),
    path('detail/<str:code>',views.courseDetail,name='detail'),
    path('delete/<str:code>',views.delete,name='delete'),
    path('courses/',include('courses.urls')),
    path('solve/',include('solve.urls')),
]
