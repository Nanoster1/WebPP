from PIL import Image
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib import admin

from .models import *


class GameAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображение размером только {}x{}'.format(
            *Game.VALID_RESOLUTION
        )

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     width_size, height_size = Game.VALID_RESOLUTION
    #     if image.size > Game.MAX_IMAGE_SIZE:
    #         raise ValidationError('Размер изображения не должен превышать 3MB!')
    #     if img.height != height_size or img.width != width_size:
    #         raise ValidationError('Разрешение изображения не допустимо!')
    #     return image


class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm


class CreatorCompanyAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображение размером только {}x{}'.format(
            *CreatorCompany.VALID_RESOLUTION
        )

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     img = Image.open(image)
    #     width_size, height_size = CreatorCompany.VALID_RESOLUTION
    #     if image.size > CreatorCompany.MAX_IMAGE_SIZE:
    #         raise ValidationError('Размер изображения не должен превышать 3MB!')
    #     if img.height != height_size or img.width != width_size:
    #         raise ValidationError('Разрешение изображения не допустимо!')
    #     return image


class CreatorCompanyAdmin(admin.ModelAdmin):
    form = CreatorCompanyAdminForm


admin.site.register(Game, GameAdmin)
admin.site.register(CategoryGame)
admin.site.register(TagsGame)
admin.site.register(CreatorGame)
admin.site.register(CreatorCompany, CreatorCompanyAdmin)
admin.site.register(FavoriteGames)
admin.site.register(Comment)
