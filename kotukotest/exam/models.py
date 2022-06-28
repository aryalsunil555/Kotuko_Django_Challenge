from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, fullname,email,password=None, password2=None):


        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            fullname = fullname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname,email,password=None):

        user = self.create_user(
            email=email,
            password=password,
            fullname=fullname
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class ToDouser(AbstractBaseUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="E-Mail Address",max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['fullname']
    
    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"

        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permission to view the app 'app_label'?"

        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class ToDOList(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/')
    deadline = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(ToDouser, related_name="todoAddedby", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-creation_date']
    def __str__(self):
        return self.name

    def get_image(data):

        from django.core.files import File
        return File(data)


