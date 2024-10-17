<template>
    <div class="song">
        <strong> {{ song.musician.musiciannickname }} - {{ song.namesong }} {{ song.songduration }}</strong>
        <my-button
            @click="songPlay"
        >
            Воспроизвести
        </my-button>
        <my-button
            v-if="isUserPage"
            @click="$emit('addText', song)"
        >
            добавить текст
        </my-button>
    </div>
</template>

<script>
import MyButton from './UI/MyButton.vue';
import store from '@/store';
export default {
    components: { MyButton },
    computed: {
        store() {
            return store
        },
        isUserPage() {
            return window.location.pathname == '/profile';
        }
    },
    props: {
        song: {
            type: Object,
            required: true
        }
    },
    methods: {
        songPlay() {
            store.dispatch('changeSong', this.song);
        }  
    }
}
</script>

<style>
.song {
    border: 1px solid #61f798;
    border-radius: 0.5em 0.1em 0.5em 0.1em;
    margin: 0.5em 0.5em 0.5em 0;
    padding-inline: 1em;
}
</style>