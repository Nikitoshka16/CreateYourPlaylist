from rest_framework import serializers
from .models import Songs, Musicians, Users
from django.conf import settings

class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musicians
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    musician = MusicianSerializer()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Songs
        fields = '__all__' 

    def get_file_url(self, obj):
        return f"{settings.MEDIA_URL}{obj.audiofile}"    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__' 
