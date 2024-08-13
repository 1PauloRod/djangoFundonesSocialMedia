from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django_countries.fields import CountryField
# Create your models here.

class ManagerCustomUser(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email or not phone_number:
            raise ValueError("Email o celular é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            phone_number=phone_number, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        user = self.create_user(
            email=email, 
            phone_number=phone_number, 
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractBaseUser):
    SELECT_CHOICES = (
        ('', 'Gênero'), 
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('P', 'Personalizado')
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True)
    bday = models.CharField(max_length=10)
    #bday = models.DateField()
    gender = models.CharField(max_length=1, choices=SELECT_CHOICES)
    
    objects = ManagerCustomUser()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]
    
    def __str__(self):
        return self.email if self.email else self.phone_number
        
        
class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    