from django.contrib.auth.base_user import BaseUserManager
 
 
class UserManager(BaseUserManager):
    user_in_migrations = True
 
    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
 
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_user(self, first_name, last_name, email, confirm_password, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(first_name, last_name, email, password, **extra_fields)
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)