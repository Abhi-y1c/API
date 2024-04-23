from django.shortcuts import render
from app.models import Student
from rest_framework.renderers import JSONRenderer
from app.serializers import StudentSerializers 
from django.http import HttpResponse,JsonResponse
import io
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
# def home(request):
#     return render(request,"home.html")

def stulist(request):
    stu_list=Student.objects.all()
    print("Query_Set=",stu_list)
    serializers=StudentSerializers(stu_list,many=True)
    print("Serializer=",serializers)
    print("python_data(serializer.data)=",serializers.data)
    json_data=JSONRenderer().render(serializers.data)
    print("Json_Data=",json_data)
    return HttpResponse(json_data,content_type='application/json')

def create(request):

     if request.method == 'POST':
        json_data=request.body
        stream= io.BytesIO(json_data)
        python_data= JSONParser().parse(stream)
        serializer =UserSerializer(data=python_data)
        if serializer.is_valid():
          serializer.save()
          res={'msg':'Data Created'}
          json_data=JSONRenderer().render(res)
          return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')