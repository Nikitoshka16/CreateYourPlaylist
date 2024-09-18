from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from .models import Musician
from .serializers import MusicianSerializer
 
@api_view(['POST', 'GET'])
def hello_world(request):
    return Response({'message': 'hello '})

@api_view(['POST', 'GET'])
def getMusicians(request):
    musicians = Musician.objects.all()
    serializer = MusicianSerializer(musicians, many=True)
    
    return Response({'musicians': serializer.data})