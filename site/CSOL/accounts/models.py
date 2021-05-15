from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to='users/', blank=True, verbose_name='Фотография')
    site = models.URLField(blank=True, null=True, verbose_name='Личный сайт')
    is_first_register = models.BooleanField(default=True, verbose_name='Первый вход')

    def __str__(self):
        return self.user.username


class Friend(models.Model):
    friends = models.ManyToManyField(Profile, default='users', blank=True, related_name='users', verbose_name='Друзья')
    current_user = models.ForeignKey(Profile, related_name='owner', on_delete=models.CASCADE, null=True, verbose_name='Пользователь')

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.friends.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.friends.remove(new_friend)

    def __str__(self):
        return 'Друзья: {}'.format(self.current_user)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
