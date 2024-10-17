<template>
    <div class="songlist">
        <song
            v-for="song in songs"
            :song="song"
            :key = "song.id"
            @addText = "$emit('addText', song)"
        >
        </song>
    </div>
</template>

<script>
import Song from './Song.vue';

export default {
    name: 'SongList',
    components: {Song},
    props: {
        songs: {
            type: Array,
            required: true
        }
    }
}
</script>

<style>
.songlist {
    overflow-y: scroll;
    height: 75vh;
}
.songlist::-webkit-scrollbar {
  width: 0.3em;
}

.songlist::-webkit-scrollbar-track {
  background: transparent; 
}
.songlist::-webkit-scrollbar-thumb {
    background-color: #61f798; 
    border-radius: 16px;
}
</style>