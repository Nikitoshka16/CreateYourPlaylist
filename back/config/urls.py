from django.contrib import admin
from django.urls import path
from app.views import getAllSongs, loginUser, set_theme, get_theme
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/allsongs/', getAllSongs),
    path('login/', loginUser),
    path('set-theme/', set_theme, name='set_theme'),
    path('get-theme/', get_theme, name='get_theme'),
]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 