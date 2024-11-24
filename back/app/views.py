from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Songs, Users, Musicians
from .serializers import SongSerializer, UserSerializer, MusicianSerializer, SongUploadSerializer, SongEditSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from django.core.exceptions import ValidationError
from mutagen import File
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema


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

def validate_token(request):
    # Извлекаем токен из заголовка Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, JsonResponse({"error": "Токен отсутствует или имеет неверный формат."}, status=401)

    token = auth_header.split(' ')[1] 
    try:
        user = Users.objects.get(token=token)
        return user, None  # Возвращаем пользователя, если токен найден
    except Users.DoesNotExist:
        return None, JsonResponse({"error": "Неверный токен."}, status=401)

# =======================================================================================
# нужные views

@api_view(['GET'])
def getAllSongs(request):
    songs = Songs.objects.select_related('musician').all();

    for song in songs:
        song.file_url = f"{settings.MEDIA_URL}{song.audiofile}"

    serializer = SongSerializer(songs, many=True)
    
    return Response({'songs': serializer.data})

@api_view(['GET'])
def search_songs(request):
    query = request.GET.get('query', '') 

    songs = Songs.objects.all()

    if query:

        songs = songs.filter(
            Q(namesong__icontains=query) | Q(musician__musiciannickname__icontains=query)
        )

    # Сериализация результатов
    serializer = SongSerializer(songs, many=True)
    
    return JsonResponse({"songs": serializer.data})

@api_view(['POST'])
def loginUser(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            user = Users.objects.get(email=email)
            if user.password == password:
                user.generate_token()
                serializer = UserSerializer(user)
                return Response({'user' : serializer.data, 'message' : 'correct', 'token' : user.token})
            else:
                return Response({'message':'incorrect'}) 
        except:
            return Response({'message':'notfound'})
    else:
        return Response({'message':'badrequest'})

@api_view(['POST'])
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

@api_view(['POST'])
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

@swagger_auto_schema(
    method='post',
    request_body=SongUploadSerializer,  
    responses={200: 'Song successfully added', 400: 'Invalid input'}
)
@api_view(['POST'])
def addSong(request):

    user, error_response = validate_token(request)
    if error_response:
        return error_response
    
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

# @api_view(['PUT'])
# def editSong(request):

    # if request.method == 'PUT':

    #     try:

    #         song = get_object_or_404(Songs, pk=request.POST.get('id'))

    #         song.namesong = request.POST.get('newnamesong')
    #         song.genre = request.POST.get('newgenre')
            
    #         new_file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST.get('newnamesong')}.mp3")

    #         # Переименовываем файл, если название изменилось
    #         old_file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST.get('oldnamesong')}.mp3")

    #         if request.POST.get('oldnamesong') != request.POST.get('newnamesong') and os.path.exists(old_file_path):
    #             os.rename(old_file_path, new_file_path)
    #             song.audiofile = f"audio_files/{request.POST.get('newnamesong')}.mp3"
            
    #         song.save()           
            
    #         return JsonResponse({"message": "success"})

    #     except ValidationError as e:
    #         return JsonResponse({"error": str(e)}, status=400)

# @api_view(['DELETE'])
# def deleteSong(request):
#     if request.method == 'DELETE':

#         try:
#             file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.data.get('namesong')}.mp3")

#             os.remove(file_path)

#             song = Songs.objects.get(pk=request.data.get('id'))
#             song.delete()
            
#             return JsonResponse({"message": "success"})

#         except Songs.DoesNotExist:
#             return JsonResponse({"error": "Song not found"}, status=404)
        

@csrf_exempt
@swagger_auto_schema(
    method='put',
    request_body=SongEditSerializer,  
    responses={200: 'Song successfully added', 400: 'Invalid input'}
)
@api_view(['GET', 'PUT', 'DELETE'])
def song_view(request, id=None):
    
    user, error_response = validate_token(request)
    if error_response:
        return error_response

    if request.method == 'POST':
        if not request.FILES.get('audiofile'):
            return JsonResponse({"error": "Файл не найден"}, status=400)

        uploaded_file = request.FILES['audiofile']
        try:
            file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST['namesong']}.mp3")
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Определяем длительность песни
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

    elif request.method == 'PUT':
        try:
            song = get_object_or_404(Songs, pk=id)
            song.namesong = request.POST.get('newnamesong', song.namesong)
            song.genre = request.POST.get('newgenre', song.genre)

            old_file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST.get('oldnamesong')}.mp3")
            new_file_path = os.path.join(settings.MEDIA_ROOT, f"audio_files/{request.POST.get('newnamesong')}.mp3")
            
            if request.POST.get('oldnamesong') != request.POST.get('newnamesong') and os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
                song.audiofile = f"audio_files/{request.POST.get('newnamesong')}.mp3"
            
            song.save()           
            
            return JsonResponse({"message": "success"})

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    elif request.method == 'DELETE':
        try:
            song = get_object_or_404(Songs, pk=id)
            file_path = os.path.join(settings.MEDIA_ROOT, song.audiofile)

            if os.path.exists(file_path):
                os.remove(file_path)

            song.delete()
            return JsonResponse({"message": "success"})

        except Songs.DoesNotExist:
            return JsonResponse({"error": "Песня не найдена"}, status=404)

    # GET: Получение информации о песне
    elif request.method == 'GET':
        
        try:

            song = Songs.objects.select_related('musician').get(pk=id)   

            serializer = SongSerializer(song)
    
            return Response({'song': serializer.data})

        except Songs.DoesNotExist:
            return JsonResponse({"error": "Песня не найдена"}, status=404)

    return JsonResponse({"error": "Метод не поддерживается"}, status=405)
