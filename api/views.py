from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status 
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import random
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()

'''class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=400)

    def get(self,request):
        query = Register.objects.all()
        serializer = RegisterSerializer(query,many=True)
        return Response(serializer.data) 

    def put(self,request,pk=None):
        try:
            register = Register.objects.get(pk=pk)
        except Register.DoesNotExist:
            return Response({'error':'Not Registered'},status=status.HTTP_200_OK)
        serializer = RegisterSerializer(register,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200) ''' 


class SubjectAndClassView(ModelViewSet):

    queryset = SubjectAndClass.objects.all()
    serializer_class = SubjectAndClassSerializer

class SectionView(ModelViewSet):

    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class SubjectView(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class AddStudentsView(ModelViewSet):
    queryset = AddStudents.objects.all()
    serializer_class = AddStudentsSerializer   

class TeachersView(ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeachersSerializer  

class BooksView(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user':{
                    'email': user.email,
                    'phone_no': user.phone_no,
                    'id': user.id,
                    'name' : user.first_name+" "+user.last_name
                }
            }) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = random.randint(0000,9999)
            user.otp = otp
            user.save()
            subject = "Your OTP"
            message = (
                f"Hi {user.first_name} {user.last_name}"
                f"Your account was registered successfully.Please enter the OTP to verify your account.\n"
                f"Your OTP is: {otp}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list= [user.email],
                fail_silently=False
            )
             
            return Response(
                {
                    "message":'User Register successful.!'
                },status=status.HTTP_201_CREATED
            ) 
        return Response(serializer.errors,status=400)                

from django.conf import settings
from django.core.mail import send_mail
import random

class SendEmailView(APIView):
    def post(self,request):
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = random.randint(0000,9999)
            subject = "Email OTP"
            message = f"This is your OTP: {otp}"
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            )
            return Response({'message':'Email send successfully.'},status=200)
        return Response(serializer.errors,status=400)  

class VerifyViewSet(APIView):
    def post(self,request):
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email,otp=otp)
                user.is_verified = True
                user.otp = None
                user.save()
                return Response({
                    "message" : f'Your eamil was verified.! : {user.email}'
                },status=200)
            except User.DoesNotExist:
                return Response({"error" : "Invalid OTP"},status=400)
        return Response(serializer.errors,status=400) 


class ResendOtpView(APIView):
    def post(self,request):
        serializer = ResendOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                if user.is_verified:
                    return Response({'message':'User already verified'},status=400)
                otp = random.randint(0000,9999)
                user.otp = otp
                user.save()

                send_mail(
                    subject=" Your OTP",
                    message=f" Your OTP is : {otp}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email,],
                    fail_silently=False
                ) 
                return Response({"message":"OTP has been resend success.!!!"},status=200)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."},status=400)
        return Response(serializer.errors,status=400)                                           





                            