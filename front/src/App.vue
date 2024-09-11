<template>
  <div>
    <h1>{{ message }} </h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: ''
    };
  },
  mounted() {
    this.HelloWorld();
  },
  methods: {
    async HelloWorld(){
      try {
          const response = await axios.get('http://localhost:8000/api/hello/');
          console.log(response)
          this.message = response.data.message
      }catch (e){
          console.log(e)
      }
    }
  }
}
</script>

<style>

</style>
