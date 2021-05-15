from PIL import Image
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

fs = FileSystemStorage(location=settings.STATIC_ROOT)


class InvalidResolutionErrorException(Exception):
    pass


class CategoryGame(models.Model):
    name = models.CharField(max_length=16, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class TagsGame(models.Model):
    name = models.CharField(max_length=16, verbose_name='Имя тега')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return "Тег: {}".format(self.name)


class Game(models.Model):
    VALID_RESOLUTION = (180, 135)
    MAX_IMAGE_SIZE = 3145728

    category = models.ForeignKey(CategoryGame, verbose_name='Категория', on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagsGame, verbose_name='Теги', blank=True)
    title = models.CharField(max_length=64, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='games/images', storage=fs, verbose_name='Иконка')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    iframe = models.URLField(verbose_name='Ссылка на IFrame')
    is_release = models.BooleanField(default=False, verbose_name='Публичный доступ')
    author = models.ForeignKey('CreatorGame', verbose_name='Автор', on_delete=models.CASCADE)
    company = models.ForeignKey('CreatorCompany', verbose_name='Компания', on_delete=models.CASCADE, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    # rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    # is_company = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def image_url(self):
        return '/' + self.image.url

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        width_size, height_size = self.VALID_RESOLUTION
        if img.height != height_size or img.width != width_size:
            raise InvalidResolutionErrorException('Разрешение изображения не допустимо!')
        super().save(*args, **kwargs)


# class ScoreBorder(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     player = models.IntegerField()
#     score = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f"Player: {self.player} | Scores: {self.score}"

class CreatorGame(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    company = models.ManyToManyField('CreatorCompany', verbose_name='Компания', blank=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return self.author.username


class CreatorCompany(models.Model):
    VALID_RESOLUTION = (512, 512)
    MAX_IMAGE_SIZE = 3145728

    name = models.CharField(max_length=64, verbose_name='Название компании')
    owner = models.ForeignKey(CreatorGame, verbose_name='Руководитель', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='games/company', storage=fs, verbose_name='Логотип')
    slug = models.SlugField(unique=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        width_size, height_size = self.VALID_RESOLUTION
        if img.height != height_size or img.width != width_size:
            raise InvalidResolutionErrorException('Разрешение изображения не допустимо!')
        super().save(*args, **kwargs)
