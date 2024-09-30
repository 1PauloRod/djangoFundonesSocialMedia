from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django_countries.fields import CountryField
from django.utils import timezone
from django.conf import settings
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
    profile_image = models.ImageField(upload_to="profile_image/", null=True, blank=True)
    objects = ManagerCustomUser()
    description_bio = models.CharField(max_length=160, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="friends_set")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]
    
    
    def __str__(self):
        return self.email if self.email else self.phone_number
        
    
    def add_friend(self, friend):
        if friend not in self.friends.all():
            self.friends.add(friend)
            friend.friends.add(self)

    def remove_friend(self, friend):
        if friend in self.friends.all():
            self.friends.remove(friend)
            friend.friends.remove(self)

    def friend_count(self):
        return self.friends.count()

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="post_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    
class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='received_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"solicitação de {self.from_user} para {self.to_user}"
    
    class Meta:
        unique_together = ('from_user', 'to_user')  # Garante que não haja duplicação de solicitações entre dois usuários