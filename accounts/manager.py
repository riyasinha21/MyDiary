from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(
        self,
        email,
        name,
        phone_number,
        password=None,
        **extra_fields
    ):

        if not email:
            raise ValueError(
                "User must have an email address"
            )

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        name,
        phone_number,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self.create_user(
            email=email,
            name=name,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )