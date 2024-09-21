from django.contrib import admin
from .models import Musicians, Musiclabels, Users, Playlists, Songs, PlaylistSongs

admin.site.register(Musicians)
admin.site.register(Musiclabels)
admin.site.register(Users)
admin.site.register(Playlists)
admin.site.register(Songs)
admin.site.register(PlaylistSongs)