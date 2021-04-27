from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=20)  # нужен размер максимальный
    description = models.TextField(blank=True)  # нужен размер максимальный
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    iframe = models.URLField()
    author = models.IntegerField()
    is_company = models.CharField(max_length=30)
    is_release = models.BooleanField(default=True)
    photo_180x135 = models.ImageField(upload_to='images/games/', width_field=180, height_field=135)
    date_added = models.DateTimeField(auto_now_add=True)


class ScoreBorder(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.IntegerField()
    score = models.IntegerField(default=0)