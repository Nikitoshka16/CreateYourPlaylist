<template>
  <div>
    <div v-for="song in songs" :key="song.id">
      <strong> {{ song.musician.musiciannickname }} - {{ song.namesong }} {{ song.songduration }}</strong>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'MainPage',
    data() {
    return {
      songs: [],
    };
  },
  mounted() {
    this.GetAllSongs();
  },
  methods: {
    async GetAllSongs(){
      try {
          const response = await axios.get('http://localhost:8000/api/allsongs/');
          console.log(response.data.songs)
          this.songs = response.data.songs
      }catch (e){
          console.log(e)
      }
    }
  }
}
</script>

<style>

</style>