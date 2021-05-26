from PIL import Image
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.urls import reverse

User = get_user_model()

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class InvalidResolutionErrorException(Exception):
    pass


class CategoryGame(models.Model):
    name = models.CharField(max_length=16, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('games:game_category', args=[self.slug])


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
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='games/images', storage=fs, verbose_name='Иконка', blank=True, default='site/no_photo_game.jpg')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    iframe = models.URLField(verbose_name='Ссылка на IFrame')
    is_release = models.BooleanField(default=False, verbose_name='Публичный доступ')
    author = models.ForeignKey('CreatorGame', verbose_name='Автор', on_delete=models.CASCADE)
    company = models.ForeignKey('CreatorCompany', verbose_name='Компания', on_delete=models.CASCADE, blank=True,
                                null=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    user_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    # rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    # is_company = models.CharField(max_length=30)

    def __str__(self):
        return self.title

    def add_view_user(self, *args, **kwargs):
        self.user_views += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('games:game_detail', args=[self.slug])

    def get_tags_all(self):
        return self.tags.all()

    # def save(self, *args, **kwargs):
    #     image = self.image
    #     img = Image.open(image)
    #     width_size, height_size = self.VALID_RESOLUTION
    #     if img.height != height_size or img.width != width_size:
    #         raise InvalidResolutionErrorException('Разрешение изображения не допустимо!')
    #     super().save(*args, **kwargs)


# class ScoreBorder(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     player = models.IntegerField()
#     score = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f"Player: {self.player} | Scores: {self.score}"

class CreatorGame(models.Model):
    profile = models.ForeignKey(Profile, verbose_name='Автор', on_delete=models.CASCADE)
    company = models.ManyToManyField('CreatorCompany', verbose_name='Компания', blank=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        return self.profile.user.username


class CreatorCompany(models.Model):
    VALID_RESOLUTION = (512, 512)
    MAX_IMAGE_SIZE = 3145728

    name = models.CharField(max_length=64, verbose_name='Название компании')
    owner = models.ForeignKey(CreatorGame, verbose_name='Руководитель', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='games/company', storage=fs, verbose_name='Логотип', default='site/no_photo.png')
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


class FavoriteGames(models.Model):
    profile = models.OneToOneField(Profile, verbose_name='Пользователь', on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, verbose_name='Игры', blank=True)

    def __str__(self):
        return "Любимые игры: {}".format(self.profile.user.username)

    def get_games_all(self):
        return self.games.all()


class Comment(models.Model):
    class Meta:
        db_table = "comments"

    # path = ArrayField(models.IntegerField())
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(verbose_name='Дата комментария', auto_now_add=True)

    def __str__(self):
        return self.content[0:200]

    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return 12 - level
