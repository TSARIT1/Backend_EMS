from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.response import Response

class RegisterView(APIView):
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
            return Response(serializer.data,status=200)  


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
    queryset = Teachers.objects.all()
    serializer_class = BooksSerializer






                            