from django.urls import path
from courses import views
from django.views.generic import RedirectView

urlpatterns = [
    path('new',views.New,name='crsnew'),
    path('<str:pk>/add',views.Add,name='crsadd'),
    path('<str:pk>/delete',views.Delete,name='crsdelete'),
    path('<str:pk>', views.Detail, name='crsinf'),
    
]
