from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'hanyuu', views.genericWs, name='generic ws'),
        url(r'^$', views.index, name='index')
]
