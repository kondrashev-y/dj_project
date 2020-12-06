from django.urls import path

from .api_views import (
    MovieListApiViews,
    MovieDetailApiViews,
    ReviewCreateApiViews,
    RatingCreateApiViews,
    ActorApiListView,
    ActorDetailApiListView,
)

urlpatterns = [
    path('movie/', MovieListApiViews.as_view(), name='movies_list'),
    path('movie/<int:pk>/', MovieDetailApiViews.as_view(), name='movie_detail'),
    path('review/', ReviewCreateApiViews.as_view()),
    path('rating/', RatingCreateApiViews.as_view(), name='rating'),
    path('actors/', ActorApiListView.as_view(), name='actor_list'),
    path('actors/<int:pk>/', ActorDetailApiListView.as_view(), name='actor_list'),
]