from django.urls import path
from choice import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.findCourse, name='findCourse'),
    path('<str:code>',views.choose,name='choose'),
]
