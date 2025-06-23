from django.db import models

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


    




