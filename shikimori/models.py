from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


#
# class ShikimoriTitleRatingManager(models.Manager):
#     def create


class ShikimoriAnimeTitle(models.Model):
    target_id = models.IntegerField(verbose_name="ID тайтла в шикимори", blank=False, unique=True)

    def __str__(self):
        return self.target_id


class ShikimoriID(models.Model):
    shikiID = models.IntegerField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class ShikimoriTitleRating(models.Model):
    title = models.ForeignKey(ShikimoriAnimeTitle, on_delete=models.CASCADE)
    owner = models.ForeignKey(ShikimoriID, on_delete=models.CASCADE, related_name='titles')
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], verbose_name="Рейтинг",
                               blank=True, null=True)

    # def __str__(self):
    #     return f'{self.title}, {self.rate}'
    def __str__(self):
        return str(self.rate)
