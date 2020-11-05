from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Genre, Actor, RingStar, Reviews, Rating, Movie, MovieShots


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1  # количество пустых дополнительных полей
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="120" height="80"')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "druft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("druft",)
    actions = ["publish", "unpublish"]
    form = MovieAdminForm
    readonly_fields = ("get_image",)
    # fields = (("actors", "directors", "genres"), ) # Будет скрывать поля которые не выбраны
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), )
        }),
        (None, {
            "fields": ("description", "poster", ("category", "get_image") )
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"), )
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "druft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="80" height="100"')



    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(druft=True)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f"{row_update} записей обновлено"
        self.message_user(request, f"{message_bit}")



    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(druft=False)
        if row_update == 1:
            message_bit = "1 запись обновлена"
        else:
            message_bit = f"{row_update} записей обновлено"
        self.message_user(request, f"{message_bit}")


    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permission = ('change', )

    publish.short_description = "Опубликовать"
    publish.allowed_permission = ('change',)

    get_image.short_description = "Постер"




@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "description", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рэйтинг"""
    list_display = ("movie", "id", "star")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("movie", "title", "description", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="60" height="40"')

    get_image.short_description = "Изображение"


# admin.site.register(Category, CategoryAdmin) # не нужна так как сделали декоратор
# admin.site.register(Genre)
# admin.site.register(Actor)
admin.site.register(RingStar)
# admin.site.register(Reviews)
# admin.site.register(Rating)
# admin.site.register(Movie)
# admin.site.register(MovieShots)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

