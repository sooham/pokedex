from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^name/(?P<name>[A-Za-z]+)/$', views.pokemon_name, name='pkmn_name'),
    # url(r'^num/(?P<num>\d+)/$', views.pokemon_no, name='pkmn_num'),
    # url(r'^about/$', views.about, name='about'),
]
