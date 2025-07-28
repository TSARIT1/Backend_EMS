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
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.core.mail import send_mail
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

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars,k=length))

class AddStudentsView(ModelViewSet):
    queryset = AddStudents.objects.all()
    serializer_class = AddStudentsSerializer   
 

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
                    'user_role': user.role,
                    'is_admin': user.is_admin(),
                    'is_teacher': user.is_teacher(),
                    'is_student': user.is_student(),
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
            print(otp)
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

from django.core.mail import send_mail
from django.conf import settings        

def send_welcome_email(email, password):
    subject = 'Your Student Account Credentials'
    message = f'''
    Welcome to our system!

    Your login credentials are:
    Email: {email}
    Password: {password}

    Please change your password after first login.
    '''
    send_mail(
        subject,
        message,
        settings.DeFAULT_FORM_EMAIL,
        [email],
        fail_silently=False,

    )

class AddStudentsView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = AddStudents.objects.all()
    serializer_class = AddStudentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        password = generate_password()
        print("password :",password)
        student = serializer.save()
        student.set_password(password)
        student.save()
        
        
        #send_welcome_email(student.email, password)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    

from rest_framework.authentication import BaseAuthentication
import jwt
from rest_framework import exceptions



class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            return None

        token = header.split()[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
            raise exceptions.AuthenticationFailed("Invalid or expired token")

        try:
            user = AddStudents.objects.get(id=payload.get('user_id'))
        except AddStudents.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        return (user, None)

class StudentLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Invalid credentials"}, status=401)

        student = serializer.validated_data['student']
        refresh = RefreshToken.for_user(student)
        refresh['user_id'] = student.id

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'student': AddStudentsSerializer(student).data
        }, status=200)

class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = request.user

        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        if not student.check_password(serializer.validated_data['old_password']):
            return Response({'detail': 'Incorrect old password'}, status=400)

        student.set_password(serializer.validated_data['new_password'])
        student.save()

        return Response({'message': 'Password updated successfully'}, status=200)



from rest_framework.permissions import IsAuthenticated,AllowAny

class TeacherViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializer

class TeacherLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        teacher = serializer.validated_data['teacher']
        refresh = RefreshToken.for_user(teacher)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'teacher': TeacherSerializer(teacher).data
        }) 

class TeacherChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            teacher = Teachers.objects.get(pk=request.user.id)
        except Teachers.DoesNotExist:
            return Response(
                {"detail": "Teacher not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not teacher.check_password(serializer.data['old_password']):
            return Response(
                {"detail": "Incorrect old password"},
                status=status.HTTP_400_BAD_REQUEST
            ) 

        teacher.set_password(serializer.data['new_password'])
        teacher.save()

        return Response(
            {"message": "Password updated successfully"},
            status=status.HTTP_200_OK
        )             






                            