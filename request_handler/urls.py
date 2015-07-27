from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sms_input_handler),
    url(r'^num/(?P<num>\d+)/$', views.pokemon_no, name='pokemon-number'),
    url(r'^about/$', views.about, name='about'),
    url(r'^help/$', views.show_help, name='help'),
]
