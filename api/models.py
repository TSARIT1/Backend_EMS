from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class SubjectAndClass(models.Model):  
    class_name  = models.CharField(max_length=255,blank=True,null=True)
    class_code  = models.CharField(max_length=255,blank=True,null=True)

class Section(models.Model):
    section_name = models.CharField(max_length=255,blank=True,null=True)
    section_code = models.CharField(max_length=255,blank=True,null=True)  

class Subject(models.Model):
    subject_name = models.CharField(max_length=255,blank=True,null=True)
    subject_code = models.CharField(max_length=255,blank=True,null=True)
    subject_credit= models.CharField(max_length=255,blank=True,null=True)
    subject_type = models.CharField(max_length=255,blank=True,null=True) 

class AddStudents(models.Model):
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    admission_no = models.CharField(max_length=255,blank=True,null=True)
    email = models.CharField(max_length=255,blank=True,null=True)
    contact = models.CharField(max_length=255,blank=True,null=True)
    blood_group = models.CharField(max_length=255,blank=True,null=True)
    skills = models.CharField(max_length=255,blank=True,null=True)
    facebook = models.CharField(max_length=255,blank=True,null=True)
    linkedin = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    zipcode = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    country = models.CharField(max_length=255,blank=True,null=True)
    father_name = models.CharField(max_length=255,blank=True,null=True)
    mother_name = models.CharField(max_length=255,blank=True,null=True)
    parent_contact = models.CharField(max_length=255,blank=True,null=True)
    parent_email = models.CharField(max_length=255,blank=True,null=True)
    parent_email = models.CharField(max_length=255,blank=True,null=True)
    additional_info = models.CharField(max_length=255,blank=True,null=True)

class Teachers(models.Model):
    select_employee_type = models.CharField(max_length=255,blank=True,null=True)
    teacher_id = models.CharField(max_length=255,blank=True,null=True)
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    contact_number = models.CharField(max_length=255,blank=True,null=True)
    email = models.CharField(max_length=255,blank=True,null=True)
    date = models.CharField(max_length=255,blank=True,null=True)
    select_gender = models.CharField(max_length=255,blank=True,null=True)
    blood_group = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    zipcode = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    country = models.CharField(max_length=255,blank=True,null=True)
    profile_summary = models.CharField(max_length=255,blank=True,null=True)
    skills = models.CharField(max_length=255,blank=True,null=True)
    facebook_profile_link = models.CharField(max_length=255,blank=True,null=True)
    linkedin_Profile_link = models.CharField(max_length=255,blank=True,null=True)  


class Books(models.Model):
    book_name = models.CharField(max_length=255,blank=True,null=True)
    books_author = models.CharField(max_length=255,blank=True,null=True)
    books_isbn = models.CharField(max_length=255,blank=True,null=True)
    books_price = models.CharField(max_length=255,blank=True,null=True)
    stock = models.CharField(max_length=255,blank=True,null=True)
    select_availability = models.CharField(max_length=255,blank=True,null=True)
    days_limit_for_check_in = models.CharField(max_length=255,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError("Superuser must have a password")

        return self.create_user(email, password, **extra_fields) 

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=225,null=True,blank=True)
    username = None
    otp = models.CharField(max_length=6,null=True,blank=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_no']

    objects = CustomUserManager()                   


    




