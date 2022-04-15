import datetime
import os
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import UserManager


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True, blank=False, null=True)
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    username = models.CharField(verbose_name='Имя пользователя', max_length=50, blank=False, null=False)
    first_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name='Имя', max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, null=False, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path, default='default.jpg')
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=False, blank=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    code = models.CharField(max_length=43, blank=False)
    shiki_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("U", "Undefined"),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_CHOICES[2][0])

    access_token = models.TextField(max_length=43, default='', blank=True)
    refresh_token = models.TextField(max_length=43, default='', blank=True)

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'code', 'date_of_birth']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']

    @property
    def age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)


class MatchRequest(models.Model):
    sender = models.ForeignKey(User, related_name='request_asker', on_delete=models.CASCADE, null=True)
    receiver = models.ForeignKey(User, related_name='request_receiver', on_delete=models.CASCADE,
                                 null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.sender) + " x " + str(self.receiver)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class MatchedUser(models.Model):
    user1 = models.IntegerField(null=True)
    user2 = models.IntegerField(null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.user1) + " x " + str(self.user2)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# # Assistance from https://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
# def image_filename(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = "%s.%s" % (uuid.uuid4(), ext)
#     return os.path.join('images/', filename)
#
#
# class UserImage(models.Model):
#     user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=image_filename, blank=True)


# class Grade(models.Model):
#     user_id_given = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_given')
#     user_id_received = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_received')
#     GRADE_CHOICES = (
#         ('U', 'Unseen'),
#         ('Y', 'Like'),
#         ('N', 'Not Like'),
#     )
#     grade = models.CharField(choices=GRADE_CHOICES, max_length=1, default=GRADE_CHOICES[0][0])
#
#     class Meta:
#         constraints = [
#             UniqueConstraint(
#                 'user_id_given',
#                 'user_id_received',
#                 name='unique_grade'
#             ),
#         ]
