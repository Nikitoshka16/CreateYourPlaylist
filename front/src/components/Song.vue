<template>
    <div class="song">
        <strong> {{ song.musician.musiciannickname }} - {{ song.namesong }} {{ song.songduration }}</strong>
        <audio controls :src="getAudioUrl(song.file_url)"></audio>
    </div>
</template>

<script>
export default {
    props: {
        song: {
            type: Object,
            required: true
        }
    },
    methods: {
        getAudioUrl(fileUrl) {
            return `http://localhost:8000${fileUrl}`;
        },
    }
}
</script>

<style>
.song {
    
}
</style>