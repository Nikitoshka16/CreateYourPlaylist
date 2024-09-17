from django.contrib import admin

# Register your models here.
from .models import Musician
# Регистрация модели MyModel для административного сайтас
admin.site.register(Musician)