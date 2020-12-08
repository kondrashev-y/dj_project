from django.urls import path

from . import views



urlpatterns = [
    path("", views.MoviesView.as_view()),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),  # поставлен специально перед урл муви слаг, для того что бы урл не попадал по запрос по фильму
    path("search/", views.Search.as_view(), name='search'),
    path("category/<slug:slug>/", views.CategoryMoviesView.as_view(), name='category_list'),
    path("rating/<int:rt>", views.RatingMovieViewList.as_view(), name='rating_list'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("movie/<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReviews.as_view(), name="add_review"),
    path("actor/<str:slug>", views.ActorView.as_view(), name='actor_detail'),
    path("actors/", views.ActorListView.as_view(), name='actor_list'),


]
