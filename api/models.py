from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
import json 

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

from django.contrib.auth.hashers import make_password,check_password    

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
    password = models.CharField(max_length=16, blank=True, null=True)

    def set_password(self,raw_password):
        self.password = make_password(raw_password)

    def check_password(self,raw_password):
        return check_password(raw_password,self.password)

    @property
    def is_authenticated(self):
        return True




class Teachers(models.Model):
    
    
    
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    employee_type = models.CharField(max_length=20,blank=True,null=True)
    teacher_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='teacher_profiles/', blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_summary = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    facebook_profile = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=16, blank=True, null=True)


            

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    @property
    def is_authenticated(self):
        return True    


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
    ADMIN = "admin"
    TEACHER = 'teacher'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (ADMIN,'admin'),
        (TEACHER,'teacher'),
        (STUDENT,'student')
    ]
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=225,null=True,blank=True)
    username = None
    otp = models.CharField(max_length=6,null=True,blank=True)
    is_verified = models.BooleanField(default=False)

    role = models.CharField(max_length=100,choices=ROLE_CHOICES,default=STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 

    def __str__(self):
        return f"{self.email} ({self.user})"

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def is_teacher(self):
        return self.role == self.TEACHER

    def is_student(self):
        return self.role == self.STUDENT 

from django.db import models
from django.utils import timezone

class EmailCampaign(models.Model):
    RECIPIENT_CHOICES = [
        ('students', 'Only Students'),
        ('teachers', 'Only Teachers'),
        ('both', 'Both Students and Teachers'),
        ('selected', 'Selected Recipients Only'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    selected_students = models.ManyToManyField('AddStudents', blank=True)
    selected_teachers = models.ManyToManyField('Teachers', blank=True)
    
    def __str__(self):
        return self.title

class Event(models.Model):
    VISIBILITY_CHOICES = [
        ('all', 'Everyone (Teachers, Students)'),
        ('teachers_only', 'Teachers Only'),
        ('students_only', 'Students Only'),
        ('students_parents', 'Students & Parents'),
        ('custom', 'Custom Selection')
    ]
    
    FREQUENCY_CHOICES = [
        ('once', 'Once'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='once')
    tags = models.CharField(blank=True,max_length=500 )  # Store as JSON string

   
    
    # For custom visibility
    visible_to_teachers = models.ManyToManyField('Teachers', blank=True)
    visible_to_students = models.ManyToManyField('AddStudents', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent = models.DateTimeField(null=True, blank=True)  


class ScheduleCategory(models.Model):
    CATEGORY_TYPES = [
        ('class_schedule', 'Class Schedule'),
        ('general_schedule', 'General Schedule'),
    ]
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    class_section = models.CharField(max_length=50, blank=True, null=True)  
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.class_section})"   


class FeesAndInvoices(models.Model):
    fee_name = models.CharField(max_length=225)
    fee_type = models.CharField(max_length=225)
    invoice_date = models.CharField(max_length=225)
    due_date = models.CharField(max_length=225)
    description = models.TextField()
    line_item = models.CharField(max_length=225)
    item_desc = models.TextField()
    settings = models.CharField(max_length=225)
    partial_payments = models.BooleanField(default=False)
    credit_balance = models.BooleanField(default=False)
    link_with_finance = models.BooleanField(default=False)
    multi_currency = models.BooleanField(default=False)  

class ManageOrgInfo(models.Model):
    institute_name = models.CharField(max_length=255)
    institute_short_name = models.CharField(max_length=255)
    sms_sender_id = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone_country_code = models.CharField(max_length=255)
    post_code = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    id_bg_color = models.CharField(max_length=255)

class Terminology(models.Model):
    students = models.CharField(max_length=255)
    parents = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    section  = models.CharField(max_length=255)
    credits_hours = models.CharField(max_length=255)
    assessment  = models.CharField(max_length=255)
    grade_book  = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    library = models.CharField(max_length=255)
    review = models.CharField(max_length=255)
    events = models.CharField(max_length=255)
    incident= models.CharField(max_length=255)
    social_learning = models.CharField(max_length=255)

    teachers = models.CharField(max_length=255)
    alumni = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)
    subjects = models.CharField(max_length=255)
    core = models.CharField(max_length=255)
    flexi_core = models.CharField(max_length=255)
    rubric  = models.CharField(max_length=255)
    report_cards = models.CharField(max_length=255)
    lecture = models.CharField(max_length=255)
    books = models.CharField(max_length=255)
    tasks = models.CharField(max_length=255)
    class_schedule = models.CharField(max_length=255)
    incident_name = models.CharField(max_length=255)




        
                     
        
                     




    




