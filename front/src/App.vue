<template>
  <div>
    <ul>
      <li v-for="musician in musicians" :key="musician.id">
        <strong>Label Name:</strong> {{ musician.labelName }}<br />
        <strong>Label Country:</strong> {{ musician.labelCountry }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      musicians: [],
    };
  },
  mounted() {
    this.HelloWorld();
  },
  methods: {
    async HelloWorld(){
      try {
          const response = await axios.get('http://localhost:8000/api/musicians/');
          console.log(response.data.musicians)
          this.musicians = response.data.musicians
      }catch (e){
          console.log(e)
      }
    }
  }
}
</script>

<style>

</style>
