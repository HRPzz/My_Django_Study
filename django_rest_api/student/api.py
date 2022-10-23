from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


class StudentList(APIView):
    # READ
    def get(self, request):
        model = Student.objects.all() # db data
        serializers = StudentSerializer(model, many=True) # db data -> json
        return Response(serializers.data) # json
    
    # CREATE
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StudentDetail(APIView):
    # READ
    def get(self, request, student_id):
        model = Student.objects.get(student_id=student_id) # db data
        serializers = StudentSerializer(model) # db data -> json
        return Response(serializers.data) # json
    
    # UPDATE    
    def put(self, request, student_id):
        model = Student.objects.get(student_id=student_id)
        serializer = StudentSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    def delete(self, request, student_id):
        model = Student.objects.get(student_id=student_id)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)