from django.urls import path
from courses import views
from django.views.generic import RedirectView

urlpatterns = [
    path('<uuid:pk>', views.Detail, name='crsinf'),
    path('<uuid:pk>/add',views.Add,name='crsadd'),
    path('<uuid:pk>/delete',views.Delete,name='crsdelete'),
    path('new',views.New,name='crsnew'),
]
