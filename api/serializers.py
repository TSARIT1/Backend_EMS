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

