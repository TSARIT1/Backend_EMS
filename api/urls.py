
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

rt = DefaultRouter()
rt.register(r'classes',SubjectAndClassView)
rt.register(r'section',SectionView, basename="section-data")
rt.register(r'subject',SubjectView,basename="subject-data")
rt.register(r'addstudents',AddStudentsView,basename="student-data")
rt.register(r'teachers',TeachersView,basename="teachers")
rt.register(r'books',BooksView,basename="books")

urlpatterns = [
    path('',include(rt.urls)),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='register'),
    path('email/',SendEmailView.as_view(),name='email'),
    path('verify/',VerifyViewSet.as_view(),name='verify-email'),
    path('resend/',ResendOtpView.as_view(),name='resend-email')
   
    
]

