<template>
  <div :class="!store.getters.getTheme ? 'app' : 'appDark'">
    <my-navbar>

    </my-navbar>
    <router-view :class="!store.getters.getTheme ? 'form' : 'formDark'">

    </router-view>
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

.appDark {
  display: grid;
  grid-template-columns: auto 1fr;
  height: 100vh;
  background: #000000;
}
.formDark {
  margin: 1em;
  border-radius: 10px;
  background: #222222;

  color:#61f798;
}
</style>
