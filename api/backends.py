from django.contrib.auth.backends import BaseBackend
from .models import AddStudents
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class StudentAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            student = AddStudents.objects.get(email=email)
            if student.check_password(password):
                return student
            return None
        except AddStudents.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AddStudents.objects.get(pk=user_id)
        except AddStudents.DoesNotExist:
            return None

from django.contrib.auth.backends import BaseBackend
from .models import Teachers, AddStudents

class CombinedAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            teacher = Teachers.objects.get(email=email)
            if teacher.check_password(password):
                return teacher
        except Teachers.DoesNotExist:
            pass

        try:
            student = AddStudents.objects.get(email=email)
            if student.check_password(password):
                return student
        except AddStudents.DoesNotExist:
            return None

    def get_user(self, user_id):

        try:
            return Teachers.objects.get(pk=user_id)
        except Teachers.DoesNotExist:
            pass
        
        try:
            return AddStudents.objects.get(pk=user_id)
        except AddStudents.DoesNotExist:
            return None            