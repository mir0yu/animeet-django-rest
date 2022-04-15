from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone_number, date_of_birth, password=None, **kwargs):
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not date_of_birth:
            raise ValueError('Users must have a date_of_birth')

        user = self.model(
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            **kwargs)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password, date_of_birth, **kwargs):
        user = self.create_user(
            phone_number=phone_number,
            username=username,
            password=password,
            date_of_birth=date_of_birth,
            is_superuser=True,
            **kwargs
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
