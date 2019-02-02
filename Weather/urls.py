from django.conf.urls import url
from Weather import views

app_name = 'Weather'

urlpatterns = [
    url('main',views.index, name='main'),
    url('delete/(?P<id>\d+)/', views.delete_city, name='delete_city'),
    url('feedback/', views.form, name='feedback'),
]
