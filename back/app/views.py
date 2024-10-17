from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .models import Songs, Users, Musicians
from .serializers import SongSerializer, UserSerializer, MusicianSerializer
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import DataForm
import xml.etree.ElementTree as ET
import os
from django.core.exceptions import ValidationError

@csrf_exempt
def set_theme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme = data.get('theme')
        if theme in [True, False]:
            response = JsonResponse({'message': 'Theme updated'})
            response.set_cookie('theme', theme, max_age=60)
            return response
        else:
            return JsonResponse({'error': 'Invalid theme'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_theme(request):
    theme = request.COOKIES.get('theme', 'false') 
    return JsonResponse({'theme': theme})

 
@api_view(['GET', 'POST'])
def getAllSongs(request):
    songs = Songs.objects.select_related('musician').all();

    for song in songs:
        song.file_url = f"{settings.MEDIA_URL}{song.audiofile}"

    serializer = SongSerializer(songs, many=True)
    
    return Response({'songs': serializer.data})

@api_view(['POST', 'GET'])
def loginUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            user = Users.objects.get(email=email)
            if user.password == password:
                serializer = UserSerializer(user)
                return Response({'user' : serializer.data, 'message' : 'correct'})
            else:
                return Response({'message':'incorrect'}) 
        except:
            return Response({'message':'notfound'})
    else:
        return Response({'message':'badrequest'})

@api_view(['POST', 'GET'])
def getMusician(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            userid = data.get('userid')
            musician = Musicians.objects.get(musicianuser=userid)

            serializer = MusicianSerializer(musician)
            return Response({'musician' : serializer.data, 'message' : 'correct'})
         
        except:
            return Response({'message':'notfound'})
    else:
        return Response({'message':'badrequest'})

@api_view(['POST', 'GET'])
def getMusicianSongs(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            musid = data.get('musid')

            songs = Songs.objects.filter(musician=musid)

            # songs = Songs.objects.get(musician=musid).all()

            serializer = SongSerializer(songs, many=True)
            return Response({'songs' : serializer.data, 'message' : 'correct'})
         
        except:
            return Response({'message':'notfound'})
    else:
        return Response({'message':'badrequest'})    

@api_view(['POST', 'GET'])
def saveTextForm(request):
    if request.method == "POST":
        form = DataForm(request.POST)
        
        if form.is_valid():

            data = form.cleaned_data

            file_path = os.path.join(settings.MEDIA_ROOT, f"{data['song']}.json")
            with open(file_path, 'w') as f:
                json.dump(data, f)
                
            return JsonResponse({"message": "success"})
        else:
            return JsonResponse({"errors": form.errors}, status=400)    

@api_view(['POST', 'GET'])
def saveTextFile(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        try:
            # Сохраняем файл на диск
            file_path = os.path.join(settings.MEDIA_ROOT, f"{request.POST['song']}.json")
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Перемещаем указатель файла в начало
            uploaded_file.seek(0)

            # Проверка валидности JSON
            try:
                json.load(uploaded_file)
            except json.JSONDecodeError:
                os.remove(file_path)
                return JsonResponse({"error": "Invalid JSON file"}, status=400)
            
            return JsonResponse({"message": "success"})

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

def list_files(request):
    folder_path = settings.MEDIA_ROOT
    files = os.listdir(folder_path)

    if not files:
        return JsonResponse({"message": "No files found"}, status=404)

    file_list = []
    for file in files:
        if file.endswith('.json'):
            file_list.append(file)
    
    return JsonResponse({"files": file_list})