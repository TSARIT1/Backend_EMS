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

class  TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = '__all__'   

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'      

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone_no','password','otp']
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
