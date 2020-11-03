from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Movie, Category, Actor, Genre, Rating
from django.views.generic.base import View
from .forms import ReviewForm, RatingForm

from django.http import HttpResponse


class GenreYear():
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(druft=False).values("year")


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(druft=False)
    paginate_by = 3
    # template_name = "movies/movies.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context["categories"] = Category.objects.all()
    #     return context


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context

# class MovieDetailView(View):
    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, "movies/movie_detail.html", {"movie": movie})

    # def get(self, request, pk):
    #     movie = Movie.objects.get(id=pk)
    #     return render(request, "movies/movie_detail.html", {"movie": movie})


class AddReviews(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk) # не надо если делать через навание столбца см ниже
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                 form.parent_id = int(request.POST.get("parent"))
            form.movie = movie  # form.movie_id = pk можно сделать через названия столбца movie_id
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере(не работает , разобраться)"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"



class ActorListView(GenreYear, DetailView):
    """Вывод информации об актере"""
    def get(self, request, name):
        actor = Actor.objects.get(name=name)
        return render(request, 'movies/actor.html', context={'actor': actor})


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 3
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()  # фильтр, там где годабудут входить в список возращаемый с фрондэнда
        return queryset

    def get_context_data(self, *agrs, **kwargs):
        context = super().get_context_data(*agrs, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(GenreYear, ListView):
    """ Поиск фильмов"""
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'{self.request.GET.get("q")}&'
        return context

    # # Поиск без учета регистра, т.к. бд sqlite не пошла c icontains
    # def get_queryset(self):
    #     q = self.request.GET.get("q")
    #     a = "".join(q[0].upper()) + q[1:]
    #     return Movie.objects.filter(title__icontains=a)



