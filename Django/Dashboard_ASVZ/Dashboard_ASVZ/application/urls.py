from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pumps/', views.pumps_view, name='pumps_view'),

]