<template>
  <div :class="!store.getters.getTheme ? 'app' : 'appDark'">
    <my-navbar>

    </my-navbar>
    
    <div>
      <router-view :class="!store.getters.getTheme ? 'form' : 'formDark'">

      </router-view>
      <div :class="!store.getters.getTheme ? 'audio-player' : 'audio-playerDark'">
        <audio 
          v-if='Object.keys(store.getters.getCurrentSong).length !== 0'
          controls :src="getAudioUrl(store.getters.getCurrentSong.file_url)"
        />
        <h1 v-else> Выберите трек!</h1>
      </div>
    </div>
  </div> 
</template>

<script>
import MyNavbar from '@/components/MyNavbar.vue';
import store from '@/store';
 
export default {
  name: 'App',
  components: { MyNavbar },
  computed: {
    store() {
      return store;
    }
  },
  data() {
    return {

    };
  },
  methods: {
    getAudioUrl(fileUrl) {
      return `http://localhost:8000${fileUrl}`;
    },
  }
}
</script>

<style>
* {
  padding: 0;
  margin: 0;
  font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}
.app {
  display: grid;
  grid-template-columns: auto 1fr;
  height: 100vh;
  background: #111113;
}
.form {
  margin: 1em;
  padding-inline: 1em;
  border-radius: 10px;
  background: #313338;

  color:#61f798;
  height: 75vh;
}

.appDark {
  display: grid;
  grid-template-columns: auto 1fr;
  height: 100vh;
  background: #000000;
}
.formDark {
  margin: 1em;
  padding-inline: 1em;
  border-radius: 10px;
  background: #222222;

  color:#61f798;
  height: 75vh;
}

.audio-player {
  margin: 1em;
  padding-inline: 1em;
  border-radius: 10px;
  background: #313338;

  color:#61f798;
  height: 15vh;
}

.audio-playerDark {
  margin: 1em;
  padding-inline: 1em;
  border-radius: 10px;
  background: #222222;

  color:#61f798;
  height: 15vh;
}
</style>
