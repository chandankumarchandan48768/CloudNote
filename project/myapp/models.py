from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_feilds):
        if not email:
            raise ValueError("Your not enterd a valid email")
        
        email= self.normalize_email(email)
        user= self.model(email= email, **extra_feilds)
        user.set_password(password)
        
        user.save(using= self._db)
        return user
    def create_user(self, email= None, password= None, **extra_feilds):
        extra_feilds.setdefault('is_staff', False)
        extra_feilds.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_feilds)    
    
    def create_superuser(self, email= None, password= None, **extra_feilds):
        extra_feilds.setdefault('is_staff', True)
        extra_feilds.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_feilds) 
    
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]
    
    email = models.EmailField(unique=True, blank=False)
    f_name = models.CharField(max_length=50, blank=False)
    l_name = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        return f"{self.f_name} {self.l_name}"

    def save(self, *args, **kwargs):
        if self.role == "admin":
            self.is_staff = True
            self.is_superuser = True
        elif self.role == "staff":
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
        
        
class Note(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='notes/')