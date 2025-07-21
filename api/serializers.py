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

class  AddStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddStudents
        fields = '__all__'

from rest_framework import serializers
from .models import Teachers

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = '__all__'
        extra_kwargs = {
            'profile_picture': {'required': False},
            'teacher_id': {'read_only': False, 'required': True},
            'email': {'required': True},
        }

    def validate_teacher_id(self, value):
        instance = getattr(self, 'instance', None)
        if instance and instance.teacher_id != value:
            if Teachers.objects.filter(teacher_id=value).exists():
                raise serializers.ValidationError("Teacher with this ID already exists.")
        return value

    def validate_email(self, value):
        instance = getattr(self, 'instance', None)
        if instance and instance.email != value:
            if Teachers.objects.filter(email=value).exists():
                raise serializers.ValidationError("Teacher with this email already exists.")
        return value   

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

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("please register")
        else:
            raise serializers.ValidationError("Must include email and password.") 
        data['user'] = user
        return data 

class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField() 

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField() 

class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()                        
