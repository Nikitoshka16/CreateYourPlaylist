from rest_framework import serializers
from .models import Songs, Musicians


class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musicians
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    musician = MusicianSerializer()

    class Meta:
        model = Songs
        fields = '__all__' 

