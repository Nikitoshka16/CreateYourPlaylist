from django.db import models


class Musiclabels(models.Model):
    id = models.BigAutoField(primary_key=True)
    labelname = models.TextField(db_column='labelName')  # Field name made lowercase.
    labelweb = models.TextField(db_column='labelWeb', blank=True, null=True)  # Field name made lowercase.
    labellogo = models.TextField(db_column='labelLogo', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    labellocate = models.TextField(db_column='labelLocate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'musicLabels'
        verbose_name = "Лейблы"
        verbose_name_plural = "Лейблы"
    
    def __str__(self):
        return self.labelname


class Musicians(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.ForeignKey(Musiclabels, models.DO_NOTHING, db_column='Label', blank=True, null=True)  # Field name made lowercase.
    musiciannickname = models.TextField(db_column='musicianNickname')  # Field name made lowercase.
    musicianuser = models.ForeignKey('Users', models.DO_NOTHING, db_column='musicianUser')  # Field name made lowercase.
    musicianisverifiedv = models.BooleanField(db_column='musicianIsVerifiedV')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'musicians'
        verbose_name = "Музыкант"
        verbose_name_plural = "Музыканты"
    
    def __str__(self):
        return self.musiciannickname


class PlaylistSongs(models.Model):
    playlist = models.OneToOneField('Playlists', models.DO_NOTHING, primary_key=True)  # The composite primary key (playlist_id, song_id) found, that is not supported. The first column is selected.
    song = models.ForeignKey('Songs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'playlist_songs'
        unique_together = (('playlist', 'song'),)
        verbose_name = "ПлейлистПесни(смеж)"
        verbose_name_plural = "ПлейлистПесни(смеж)"
    
    def __str__(self):
        return self.playlist


class Playlists(models.Model):
    id = models.BigAutoField(primary_key=True)
    playlistname = models.TextField(db_column='playlistName')  # Field name made lowercase.
    playlistpreview = models.TextField(db_column='playlistPreview', blank=True, null=True)  # Field name made lowercase.
    playlistowner = models.ForeignKey('Users', models.DO_NOTHING, db_column='playlistOwner', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'playlists'
        verbose_name = "Плейлисты"
        verbose_name_plural = "Плейлисты"
    
    def __str__(self):
        return self.playlistname


class Songs(models.Model):
    id = models.BigAutoField(primary_key=True)
    musician = models.ForeignKey(Musicians, models.DO_NOTHING, db_column='musician')
    namesong = models.TextField(db_column='nameSong')  # Field name made lowercase.
    genre = models.TextField(blank=True, null=True)
    audiofile = models.TextField(db_column='audioFile', blank=True, null=True)  # Field name made lowercase.
    songpreview = models.TextField(db_column='songPreview', blank=True, null=True)  # Field name made lowercase.
    songrealeasedatee = models.DateField(db_column='songRealeaseDatee')  # Field name made lowercase.
    songduration = models.DurationField(db_column='songDuration')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'songs'
        verbose_name = "Песни"
        verbose_name_plural = "Песни"
    
    def __str__(self):
        return self.namesong


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.TextField()
    password = models.TextField()
    username = models.TextField()
    userdatereg = models.DateField(db_column='userDateReg', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return self.username
