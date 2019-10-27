from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('campaign/<str:campaign_id>/', views.campaign, name='campaign'),

    path('graph/', views.graph, name='graph'),

    path('api/graph/campaigns/', views.graph_campaigns,
         name='graph_campaigns'),

    path('api/graph/connections/',
         views.graph_connections,
         name='graph_connections'),
]
