from django.contrib import admin
from django.urls import path
from app.views import getAllSongs, loginUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/allsongs/', getAllSongs),
    path('login/', loginUser)
]
 