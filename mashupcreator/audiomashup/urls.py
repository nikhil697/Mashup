from django.urls import path,include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [

    path('',views.index,name='index'),
    path('mix',views.mixer,name='mix'),
]