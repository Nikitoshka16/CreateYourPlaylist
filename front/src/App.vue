<template>
  <div class="app">
    <my-navbar>

    </my-navbar>
    <router-view class="form">

    </router-view>
  </div> 
</template>

<script>
import MyNavbar from '@/components/MyNavbar.vue';

 
export default {
  name: 'App',
  components: { MyNavbar },
  data() {
    return {

    };
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
  border-radius: 10px;
  background: #313338;

  color:#61f798;
}
</style>
