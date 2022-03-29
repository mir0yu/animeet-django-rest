import datetime
import os
import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    def create_user(self, phone_number, password=None, **kwargs):
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone_number=phone_number, **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password, **kwargs):
        user = self.create_user(
            phone_number=phone_number,
            username=username,
            password=password,
            is_superuser=True,
            **kwargs
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    username = models.CharField('username', max_length=50, blank=False, null=False)
    first_name = models.CharField('Фамилия', max_length=255, blank=True, null=True)
    last_name = models.CharField('Имя', max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')
    date_of_birth = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    last_time_visit = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    code = models.CharField(max_length=43, blank=False)
    shiki_id = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    GENDER_CHOICES = (
        ('M', 'Муж'),
        ('F', 'Жен'),
    )

    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)

    access_token = models.TextField(max_length=43, default='', blank=True)
    refresh_token = models.TextField(max_length=43, default='', blank=True)

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'code', ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)


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


class Grade(models.Model):
    user_id_given = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_given')
    user_id_received = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_received')
    GRADE_CHOICES = (
        ('U', 'Unseen'),
        ('Y', 'Like'),
        ('N', 'Not Like'),
    )
    grade = models.CharField(choices=GRADE_CHOICES, max_length=1, default=GRADE_CHOICES[0][0])

    class Meta:
        constraints = [
            UniqueConstraint(
                'user_id_given',
                'user_id_received',
                name='unique_grade'
            ),
        ]
