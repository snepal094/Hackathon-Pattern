
from django.urls import path 
from .import views
from .views import  home, generate_regex 

urlpatterns=[
    path('',home,name='home'),
    path('generate_regex/',generate_regex, name='generate_regex')
]