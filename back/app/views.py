from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .models import Songs, Users
from .serializers import SongSerializer, UserSerializer
from django.http import JsonResponse
import json

@api_view(['GET', 'POST'])
def getAllSongs(request):
    songs = Songs.objects.select_related('musician').all();
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