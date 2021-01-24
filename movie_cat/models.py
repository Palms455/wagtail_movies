from django.db import models
from django import forms

from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from datetime import date


@register_snippet
class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Наименование", max_length=150)
    description = models.TextField("Описание")

    panels = [
        FieldPanel('name'),
        FieldPanel('description')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        db_table = "'catalog.genre'"



@register_snippet
class Category(models.Model):
    """Категории"""
    name = models.CharField("Наименование", max_length=150)
    description = models.TextField("Описание")

    panels = [
        FieldPanel('name'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "'catalog.category'"


class Actor(Page):
    """Актеры и режиссеры"""
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('age'),
        ImageChooserPanel('image'),
        FieldPanel('description'),
    ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.title})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"
        db_table = "'catalog.actor'"


class Movie(Page):
    """Фильм"""
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = RichTextField("Описание", blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    movie_category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.SearchField('year'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('tagline'),
        ImageChooserPanel('image'),
        FieldPanel('year'),
        FieldPanel('country'),
        FieldPanel('actors'),
        InlinePanel('gallery_images', label='Кадры из фильма'),
        InlinePanel('ratings', label='Рейтинг'),
        InlinePanel('reviews', label='Отзывы'),
        FieldPanel('movie_category', widget=forms.CheckboxSelectMultiple),
        FieldPanel('genres', widget=forms.CheckboxSelectMultiple),
    ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        db_table = "'catalog.movie'"


class MovieShots(Orderable):
    """Кадры из фильма"""
    description = models.TextField("Описание")
    movie = ParentalKey(Movie, verbose_name="Фильм", null=True, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('description'),
    ]


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"
        db_table = "'catalog.movie_shots'"


class RatingStar(Orderable):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]
        db_table = "'catalog.rating_star'"


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = ParentalKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="фильм",
        related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
        db_table = "'catalog.rating'"


class Review(Orderable):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    movie = ParentalKey(Movie, verbose_name="фильм", on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        db_table = "'catalog.reviews'"