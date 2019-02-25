from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'campaign/search/', views.campaign_search,
        name='campaign_search'),
    path(
        'campaign/<str:campaign_id>/', views.campaign,
        name='campaign'),
]
