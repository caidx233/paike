from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from solve import views
urlpatterns = [
    path('',views.slv,name='slv'),
]
