from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .models import Songs
from .serializers import SongSerializer
 
@api_view(['POST', 'GET'])
def hello_world(request):
    return Response({'message': 'hello '})

@api_view(['GET', 'POST'])
def getAllSongs(request):
    songs = Songs.objects.select_related('musician').all();
    serializer = SongSerializer(songs, many=True)
    
    return Response({'songs': serializer.data})

