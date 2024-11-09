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
from mutagen import File
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.db.models import Q

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


@api_view(['POST', 'GET'])
def addSong(request):

    if request.method == 'POST' and request.FILES.get('audiofile'):
        uploaded_file = request.FILES['audiofile']

        try:
            file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST['namesong']}.mp3")

            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            

            audio = File(file_path)
            
            if audio is None or not hasattr(audio.info, 'length'):
                return JsonResponse({"error": "Невозможно определить продолжительность аудиофайла."}, status=400)
            
            song_duration = timedelta(seconds=int(audio.info.length))


            song = Songs.objects.create(
                musician=get_object_or_404(Musicians, pk=request.POST.get('musician')),
                namesong=request.POST['namesong'],
                genre=request.POST['genre'],
                audiofile=f"audio_files/{request.POST['namesong']}.mp3",
                songpreview=None,  
                songrealeasedatee=datetime.today().strftime("%Y-%m-%d"),
                songduration=song_duration,
            )
           
            
            return JsonResponse({"message": "success"})

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

@api_view(['PUT'])
def editSong(request):

    if request.method == 'PUT':

        try:

            song = get_object_or_404(Songs, pk=request.POST.get('id'))

            song.namesong = request.POST.get('newnamesong')
            song.genre = request.POST.get('newgenre')
            
            new_file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST.get('newnamesong')}.mp3")

            # Переименовываем файл, если название изменилось
            old_file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST.get('oldnamesong')}.mp3")

            if request.POST.get('oldnamesong') != request.POST.get('newnamesong') and os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
                song.audiofile = f"audio_files/{request.POST.get('newnamesong')}.mp3"
            
            song.save()           
            
            return JsonResponse({"message": "success"})

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

@api_view(['DELETE'])
def deleteSong(request):
    if request.method == 'DELETE':

        try:
            file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.data.get('namesong')}.mp3")

            os.remove(file_path)

            song = Songs.objects.get(pk=request.data.get('id'))
            song.delete()
            
            return JsonResponse({"message": "success"})

        except Songs.DoesNotExist:
            return JsonResponse({"error": "Song not found"}, status=404)
        
@api_view(['GET'])
def search_songs(request):
    query = request.GET.get('query', '')  # Название песни или имя музыканта

    # Начинаем с получения всех песен
    songs = Songs.objects.all()

    # Если задан запрос
    if query:
        # Используем Q объекты для поиска по обеим полям с логикой OR
        songs = songs.filter(
            Q(namesong__icontains=query) | Q(musician__musiciannickname__icontains=query)
        )

    # Сериализация результатов
    serializer = SongSerializer(songs, many=True)
    
    return JsonResponse({"songs": serializer.data})