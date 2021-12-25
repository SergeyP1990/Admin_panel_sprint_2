import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_('title'), max_length=255)
    birth_date = models.DateField(_('birth date'), blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = "content\".\"person"


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    WRITER = 'writer', _('Writer')
    DIRECTOR = 'director', _('Director')

class FilmworkPerson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Person'

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [models.UniqueConstraint(fields=['film_work', 'person', 'role'], name='film_work_person_role')]


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = "content\".\"genre"


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Genre'

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [models.UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre')]


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')



class Filmwork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    certificate = models.TextField(_('certificate'), blank=True)
    file_path = models.FileField(_('file'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('rating'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('type'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')
    persons = models.ManyToManyField(Person, through='FilmworkPerson')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = "content\".\"film_work"
