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

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailCampaign, AddStudents, Teachers
from .serializers import EmailCampaignSerializer, SimpleStudentSerializer, SimpleTeacherSerializer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import permissions

class EmailCampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = EmailCampaign.objects.all().order_by('-created_at')
    serializer_class = EmailCampaignSerializer

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        campaign = self.get_object()
        try:
            success = self.send_campaign_emails(campaign)
            if success:
                return Response({'status': 'emails sent successfully'}, status=status.HTTP_200_OK)
            return Response({'status': 'no valid recipients found'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def send_campaign_emails(self, campaign):
        subject = campaign.title
        message = campaign.description
        from_email = settings.EMAIL_HOST_USER
        recipient_list = []

        # Get recipients based on campaign type
        if campaign.recipient_type == 'students':
            students = AddStudents.objects.exclude(email__isnull=True).exclude(email__exact='')
            recipient_list.extend([student.email for student in students if self.is_valid_email(student.email)])
        
        elif campaign.recipient_type == 'teachers':
            teachers = Teachers.objects.all()
            recipient_list.extend([teacher.email for teacher in teachers])
        
        elif campaign.recipient_type == 'both':
            students = AddStudents.objects.exclude(email__isnull=True).exclude(email__exact='')
            teachers = Teachers.objects.all()
            recipient_list.extend([student.email for student in students if self.is_valid_email(student.email)])
            recipient_list.extend([teacher.email for teacher in teachers])
        
        elif campaign.recipient_type == 'selected':
            selected_students = campaign.selected_students.exclude(email__isnull=True).exclude(email__exact='')
            selected_teachers = campaign.selected_teachers.all()
            recipient_list.extend([student.email for student in selected_students if self.is_valid_email(student.email)])
            recipient_list.extend([teacher.email for teacher in selected_teachers])

        # Remove duplicates and send
        recipient_list = list(set(filter(None, recipient_list)))
        
        if recipient_list:
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            campaign.sent_at = timezone.now()
            campaign.save()
            return True
        return False

    def is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @action(detail=False, methods=['get'])
    def recipient_options(self, request):
        students = AddStudents.objects.exclude(email__isnull=True).exclude(email__exact='')
        teachers = Teachers.objects.all()
        
        student_serializer = SimpleStudentSerializer(students, many=True)
        teacher_serializer = SimpleTeacherSerializer(teachers, many=True)
        
        return Response({
            'students': student_serializer.data,
            'teachers': teacher_serializer.data
        })

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, Teachers, AddStudents
from .serializers import EventSerializer
from django.utils import timezone

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    
    queryset = Event.objects.all().order_by('-start_date')
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        event = self.get_object()
        try:
            self.send_event_notification(event)
            return Response({'status': 'event notifications sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def send_event_notification(self, event):
        subject = f"Event Notification: {event.title}"
        
        message = f"""
        {event.description}
        
        Date: {event.start_date.strftime('%A, %B %d, %Y')}
        Time: {event.start_date.strftime('%I:%M %p')} to {event.end_date.strftime('%I:%M %p')}
        Location: {event.location}
        Event Type: {event.event_type}
        
        {'(Recurring: ' + event.get_frequency_display() + ')' if event.frequency != 'once' else ''}
        """
        
        recipient_list = []
        
        if event.visibility == 'all':
            teachers = Teachers.objects.all()
            students = AddStudents.objects.exclude(email__isnull=True).exclude(email__exact='')
            recipient_list.extend([t.email for t in teachers])
            recipient_list.extend([s.email for s in students])
            
        elif event.visibility == 'teachers_only':
            teachers = Teachers.objects.all()
            recipient_list.extend([t.email for t in teachers])
            
        elif event.visibility == 'students_only':
            students = AddStudents.objects.exclude(email__isnull=True).exclude(email__exact='')
            recipient_list.extend([s.email for s in students])
            
        elif event.visibility == 'students_parents':
            students = AddStudents.objects.exclude(email__isnull=True).exclude(email__exact='')
            recipient_list.extend([s.email for s in students])
            # Add parent emails where available
            recipient_list.extend([
                s.parent_email for s in students 
                if s.parent_email and s.parent_email.strip()
            ])
            
        elif event.visibility == 'custom':
            teachers = event.visible_to_teachers.all()
            students = event.visible_to_students.exclude(email__isnull=True).exclude(email__exact='')
            recipient_list.extend([t.email for t in teachers])
            recipient_list.extend([s.email for s in students])
            # Include parent emails for selected students
            recipient_list.extend([
                s.parent_email for s in students 
                if s.parent_email and s.parent_email.strip()
            ])
        
        # Remove duplicates and empty emails
        recipient_list = list(set(filter(None, recipient_list)))
        
        if recipient_list:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            event.last_sent = timezone.now()
            event.save()

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        now = timezone.now()
        upcoming_events = Event.objects.filter(
            start_date__gte=now,
            start_date__lte=now + timezone.timedelta(days=30)
        ).order_by('start_date')
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)

class ScheduleCategoryViewSet(viewsets.ModelViewSet):
    queryset = ScheduleCategory.objects.all().order_by('-start_date')
    serializer_class = ScheduleCategorySerializer
    permission_classes = [permissions.AllowAny]  


class FeesAndInvoicesViewSet(viewsets.ModelViewSet):
    queryset = FeesAndInvoices.objects.all()
    serializer_class = FeesAndInvoiceSerializer
    permission_classes = [permissions.AllowAny]
                               
class ManageOrgInfoViewSet(viewsets.ModelViewSet):
    queryset = ManageOrgInfo.objects.all()
    serializer_class = ManageOrgInfoSerializer
    permission_classes = [permissions.AllowAny]

class TerminologyViewSet(viewsets.ModelViewSet):
    queryset =Terminology.objects.all()
    serializer_class = TerminologySerializer
    permission_classes = [permissions.AllowAny]






                            