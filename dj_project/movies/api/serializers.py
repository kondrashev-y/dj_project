from rest_framework import serializers

from ..models import Movie, Category, Actor, Reviews, Rating


class CategorySerializer(serializers.ModelSerializer):
    """Список катеогрий"""

    class Meta:
        model = Category
        fields = ('name',)


class ActorSerializer(serializers.ModelSerializer):
    """Список Актеров и Режиссеров"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')

class ActorDetailSerializer(serializers.ModelSerializer):
    """Список Актеров и Режиссеров"""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""

    category = CategorySerializer()
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавления отзыва"""

    class Meta:
        model = Reviews
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр коментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзыва"""

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Reviews
        fields = ('name', 'text', 'children')


class MovieDetailsSerializer(serializers.ModelSerializer):
    """Информация о фильме"""

    # category = CategorySerializer()
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    actors = ActorSerializer(read_only=True, many=True)
    # actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    directors = ActorSerializer(read_only=True, many=True)
    # directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('druft',)


class RatingCreateSerializer(serializers.ModelSerializer):
    """Добавление рейтинга по API"""

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(  # rating = Rating...... когда не было CreateApiView
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating


