from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('candidate/<str:candidate_id>/', views.candidate, name='candidate'),
    path('graph/', views.graph, name='graph'),
    path(
        'api/graph/candidates/',
        views.graph_candidates,
        name='graph_candidates'),
    path(
        'api/graph/connections/',
        views.graph_connections,
        name='graph_connections'),
]
