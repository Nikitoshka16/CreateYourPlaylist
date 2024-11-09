<template>
  <div>

    <div class="searchForm">
      <div class="searchForm">
      <my-input
        id="searchText"
        :modelValue="searchText"
        @update:modelValue="newValue => searchText = newValue"
        placeholder="Поиск..."
        name="search_field"
        autocomplete="new-password"
        autocorrect="off"
        @input="searchSongs" 
      />
    </div>
    </div>

    <div class="list">
      <song-list
        :songs="songs"
      />
    </div>
    <div @click="store.dispatch('changeFormAuth')" v-show="store.getters.getFormAuth" class="modal-background"></div>

    <div v-show="store.getters.getFormAuth" class="auth">

      <h1>Авторизация</h1>

      <div class="authForm">
        <my-input
          :modelValue="email"
          @update:modelValue="newValue => email = newValue"
          placeholder="Введите email"
          name="email"
          autocomplete="username"
        />
        <my-input
          :modelValue="password"
          @update:modelValue="newValue => password = newValue"
          placeholder="Введите пароль"
          :isPassword="true"
          name="password"
          autocomplete="new-password"
        />
        <div>
          <my-button
            @click="AuthUser"
          >
          Войти
          </my-button>
          <my-button>Регистрация</my-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SongList from '@/components/SongList.vue';
import store from '@/store';
import axios from 'axios'
import MyInput from '../components/UI/MyInput.vue';
import MyButton from '../components/UI/MyButton.vue';
import router from '@/router/router';
export default {
  components: { MyInput, MyButton, SongList},
    name: 'MainPage',
    computed: {
      store() {
        return store
      }
    },
    data() {
    return {
      songs: [],
      email: '',
      password: '',
      searchText: '',
    };
  },
  mounted() {
    this.GetAllSongs();
  },
  methods: {
    async searchSongs() {
      
      if (this.searchText.trim()) { 
        try {
          
          const response = await axios.get('http://localhost:8000/search-songs/', {
            params: { query: this.searchText } 
          });
          this.songs = response.data.songs;
        } catch (error) {
          console.error('Ошибка при поиске:', error);
        }
      } else {
        this.GetAllSongs(); 
      }
    },
    async GetAllSongs(){
      try {
          const response = await axios.get('http://localhost:8000/api/allsongs/');
          this.songs = response.data.songs;
          console.log(this.songs);
      }catch (e){
          console.log(e);
      }
    },
    AuthUser() {
      axios.post('http://localhost:8000/login/', {email: this.email, password: this.password})
      .then(res => {
        if (res.status === 200 && res.data.message === 'correct') {
          store.dispatch('changeIsAuth');
          store.dispatch('changeFormAuth');
          this.password = '';
          this.email = '';
          console.log(res.data.user);
          store.dispatch('setUser', res.data.user);
          router.push('/profile');
        }
        else if (res.status === 200 && res.data.message === 'incorrect'){
          alert('Неверный пароль');
        }
        else if (res.status === 200 && res.data.message === 'notfound'){
          alert('Пользователя с таким email не существует');
        }
        else if (res.status === 200 && res.data.message === 'badrequest'){
          alert('неверный метод запроса');
        }
      })
      
    }
  }
}
</script>

<style scoped>
.auth {
  background: rgb(50, 50, 50);
  border: 1px solid #61f798;
  border-radius: 1em;
  width: 300px;
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}
.modal-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8); /* Затемнённый фон */
  z-index: 999;
}
.authForm {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
.searchForm {
  height: 10vh;
  padding-right: 1em;
}
</style>