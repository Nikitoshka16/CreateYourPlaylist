<template>
  <div class="navbar">
      <div>
          МЕСТО ДЛЯ ЛОГО
      </div>
      <div>
          <button
                  @click="$router.push({
                  name: 'mailingPage',
                   params: {
                      id : this.$route.params['id'],
                      role: this.$route.params['role']
                  }
                  })"
                  style="margin-left: 20px"
          >
              Рассылка
          </button>

          <button
              v-show="!store.getters.getIsAuth"
              @click="$router.push('/login')"
              style="margin-left: 20px"
          >
              Авторизация
          </button>
          <button
              v-show="store.getters.getIsAuth"
              @click="exitUser"
              style="margin-left: 20px"
          >
              Выйти
          </button>
      </div>
  </div>
</template>

<script>

import router from "@/router/router";

export default {
    name: "my-navbar",
    computed: {
        store() {
            return store
        }
    },
    components: {MyButton},
    methods: {
        exitUser(){
            router.push('/login')
            store.dispatch('changeIsAuth')
            store.dispatch('changeIsAuthAdmin')
        }
    }
}
</script>

<style scoped>
.navbar{
    height: 70px;
    background-color: lightblue;
    box-shadow: 2px 2px 4px gray;
    display: flex;
    align-items: center;
    padding: 0 15px;
}
.navbar__btns{
    margin-left: auto;
}
</style>