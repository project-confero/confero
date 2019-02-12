from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('politician/<int:politician_id>/', views.politician, name='politician'),
]
