from django.contrib import admin
from django.urls import path, re_path
from app.views import (
   getAllSongs, 
   loginUser, 
   getMusician, 
   getMusicianSongs, 
   song_view, 
   search_songs,
   addSong
)
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="УЖАС КАКОЙ ТО",
      default_version='v777',
      description="получить поменять удалить там сям",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('admin/', admin.site.urls),

   path('login/', loginUser),
   path('getMusician/', getMusician),
   path('getMusicianSongs/', getMusicianSongs), 

   path('allsongs/', getAllSongs),
   path('search-songs/', search_songs),

   path('song/<int:id>/', song_view),
   path('addSong/', addSong),

   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
   
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    

   