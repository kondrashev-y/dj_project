from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework import permissions

from ..models import Movie, Actor, Reviews
from .serializers import (
    MovieListSerializer,
    MovieDetailsSerializer,
    ReviewCreateSerializer,
    RatingCreateSerializer,
    ActorSerializer,
    ActorDetailSerializer,
    ReviewSerializer,
)

from .service import get_client_ip, MovieFilter

from django_filters.rest_framework import DjangoFilterBackend


class MovieListApiViews(ListAPIView):
    """Вывод списков фильмов в API"""

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(druft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            # middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
            middle_star=models.Avg('ratings__star')
        )
        return movies


# class MovieDetailApiViews(APIView):
#     """Вывод детальной информации в API"""
#     def get(self, request, pk):
#         movies = Movie.objects.get(druft=False, id=pk)
#         serializer = MovieDetailsSerializer(movies)
#         return Response(serializer.data)

class MovieDetailApiViews(RetrieveAPIView):
    """Вывод детальной информации в API"""

    queryset = Movie.objects.filter(druft=False)
    serializer_class = MovieDetailsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewDestroy(DestroyAPIView):
    """Удаление отзыва"""
    queryset = Reviews.objects.all()
    # permission_classes = ReviewSerializer
    permission_classes = [permissions.IsAdminUser]


# class ReviewCreateApiViews(APIView):
#     """Добавление отзыва к фильму"""
#
#     def post(self, request):
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)

class ReviewCreateApiViews(CreateAPIView):
    """Добавление отзыва к фильму"""

    serializer_class = ReviewCreateSerializer

# class RatingCreateApiViews(APIView):
#     """Добавление рейтинга к фильму"""
#
#     def post(self, request):
#         serializer = RatingCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)

class RatingCreateApiViews(CreateAPIView):
    """Добавление рейтинга к фильму"""

    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorApiListView(ListAPIView):
    """Вывод списка актеров"""
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class ActorDetailApiListView(RetrieveAPIView):
    """Вывод информации об актере"""
    serializer_class = ActorDetailSerializer
    queryset = Actor.objects.all()
    lookup_field = 'pk'
