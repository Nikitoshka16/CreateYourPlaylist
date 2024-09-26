<template>
    <div class="header">

        <div class="navbar">

            <img class="logo" src="../assets/logo.png" alt="logo">

            <my-button
                  @click="$router.push({
                  name: 'mainPage'})"

            >
            Главная
            </my-button>
 
            <my-button
                @click="$router.push({
                    name: 'playlistPage',
                    params: {
                        id : this.$route.params['id']
                    }
                })"
            >
            Плейлисты
            </my-button>     

        </div>

        <div class="auth">

            <my-button
              v-show="!store.getters.getIsAuth"
              @click="loginUser"
            >
            Авторизация
            </my-button>

            <my-button
              v-show="store.getters.getIsAuth"
              @click="$router.push({
                    name: 'userPage',
                    params: {
                        id : this.$route.params['id']
                    }
                })"
            >
                <img src="../assets/user.png" alt="profile icon">
                {{ store.getters.getUser.username}}
            </my-button>

        </div>
    </div>
</template>

<script>

import MyButton from "@/components/UI/MyButton.vue";
import store from "@/store";
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
            router.push('/')
            store.dispatch('changeIsAuth')
        },
        loginUser() {
            store.dispatch('changeFormAuth')
        }
    }
}
</script>

<style scoped>
.header{
    padding: 1em;
    padding-inline: 2em;
    background: transparent;
    height: 100vh-2em;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.navbar {
    display: flex;
    flex-direction: column;
}
.logo {
    width: 10em;
    padding-bottom: 2em;
}
img {
    width: 5em;
}
</style>