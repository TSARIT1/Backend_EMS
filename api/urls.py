
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

rt = DefaultRouter()
rt.register(r'classes',SubjectAndClassView)
rt.register(r'sections',SectionView, basename="section-data")
rt.register(r'subjects',SubjectView,basename="subject-data")
rt.register(r'addstudents',AddStudentsView,basename="student-data")
rt.register(r'teachers', TeacherViewSet, basename='teacher')
rt.register(f'students', AddStudentsView,basename='students')

rt.register(r'books',BooksView,basename="books")

urlpatterns = [
    path('',include(rt.urls)),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='register'),
    path('email/',SendEmailView.as_view(),name='email'),
    path('verify/',VerifyViewSet.as_view(),name='verify-email'),
    path('resend/',ResendOtpView.as_view(),name='resend-email'),

    path('student/login/', StudentLoginView.as_view(), name='student-login'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    
    path('teacherss/login/', TeacherLoginView.as_view(), name='teacher-login'),
    path('teacherss/change-password/', TeacherChangePasswordView.as_view(), name='teacher-change-password'),
   
    
]

