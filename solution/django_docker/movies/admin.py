from django.contrib import admin

from .models import Filmwork, FilmworkGenre, Person, Genre, FilmworkPerson


class FilmworkGenreInline(admin.TabularInline):
    model = FilmworkGenre
    extra = 0


class FilmworkPersonInline(admin.TabularInline):
    model = FilmworkPerson
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating',)
    fields = (
            'title', 'type', 'description', 'creation_date', 'certificate',
            'file_path', 'rating',
        )
    search_fields = ('title', 'description', 'id',)

    inlines = [
        FilmworkGenreInline, FilmworkPersonInline
    ]


@admin.register(Person)
class Person(admin.ModelAdmin):
    search_fields = ('full_name', 'id')


@admin.register(Genre)
class Genre(admin.ModelAdmin):
    search_fields = ('name', 'id')
