from django.contrib.auth.base_user import BaseUserManager


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
