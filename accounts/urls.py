from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^login', views.log_in, name='login'),
        url(r'^signup', views.sign_up, name='signup'),
        url(r'^logout', views.log_out, name='logout')
]