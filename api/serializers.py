from rest_framework import serializers
from .models import * 

class SubjectAndClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectAndClass
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'    

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'  

import random
import string

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError    

class  AddStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddStudents
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate_email(self,value):
        try:
            validate_email(value)
            return value
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")     

from rest_framework import serializers
from .models import Teachers



def generate_password_teacher(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = '__all__'
        extra_kwargs = {
            'password': {'read_only': True}
        }
    def create(self,validated_data):
        validated_data['password'] = generate_password_teacher()
        return super().create(validated_data) 
       

       

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'      

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone_no','password','role']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

from django.contrib.auth import authenticate  
                      
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        try:
            student = AddStudents.objects.get(email=email)
        except AddStudents.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not student.check_password(password):
            raise serializers.ValidationError("Invalid credentials")            

        data['student'] = student
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    def validate(self,data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField() 

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField() 

class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()  


def generate_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = generate_password()
        print("password : ",password)
        teacher = Teachers(**validated_data)
        teacher.set_password(password)
        teacher.save()
        return teacher

class TeacherLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            teacher = Teachers.objects.get(email=email)
            if not teacher.check_password(password):
                raise serializers.ValidationError("Invalid credentials")
            data['teacher'] = teacher
            return data
        except Teachers.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")


class TeacherChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True, min_length=8)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

from rest_framework import serializers
from .models import EmailCampaign, AddStudents, Teachers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class EmailCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCampaign
        fields = '__all__'
        extra_kwargs = {
            'sent_at': {'read_only': True},
        }

    def validate(self, data):
        if data.get('recipient_type') == 'selected':
            if not data.get('selected_students') and not data.get('selected_teachers'):
                raise serializers.ValidationError("For 'selected' recipient type, you must select at least one student or teacher.")
        return data

class SimpleStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddStudents
        fields = ['id', 'first_name', 'last_name', 'email','parent_email','father_name','mother_name','admission_no']

class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = ['id', 'first_name', 'last_name', 'email']                                                          


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'last_sent': {'read_only': True},
            'created_at': {'read_only': True}
        }

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class ScheduleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCategory
        fields = '__all__'    


class FeesAndInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesAndInvoices
        fields = '__all__'

class ManageOrgInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageOrgInfo
        fields = '__all__'

class TerminologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminology
        fields = '__all__'
