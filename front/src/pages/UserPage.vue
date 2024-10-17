<template>
  <div>
    <!-- <my-button 
    @click="toggleTheme"
    >
    {{ store.getters.getTheme == false ? 'Switch to MORE DARK Theme' : 'Switch to Dark Theme' }}
    </my-button> -->
    <div class="list">
      <song-list
        @addText="addText"
        :songs="songs"
      />
    </div>

    <div @click="this.addText" v-show="this.isFormAddText" class="addTextBackground"></div>
    <div v-show="this.isFormAddText" class="addText">

      <h1>Заполните форму или выберите файл</h1>

      <div class="addTextForm">
        <div clas="inputForm">
          <my-input
            :modelValue="str1"
            @update:modelValue="newValue => str1 = newValue"
            placeholder="Введите строку 1"
            required
          />
          <my-input
            :modelValue="str2"
            @update:modelValue="newValue => str2 = newValue"
            placeholder="Введите строку 2"
          />

          <my-button
            @click="saveTextForm"
          >
            Сохранить c формы
          </my-button>
        </div>
        <div class="fileForm">
          <input type="file" @change="onFileChange">
          <my-button
            @click="saveTextFile"
          >
            Сохранить файл
          </my-button>
        </div>
        <div>
          <ul v-if="files.length > 0">
            <li v-for="file in files" :key="file">{{ file }}</li>
          </ul>
          <p v-else>пусто.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import store from '@/store';
import MyButton from '../components/UI/MyButton.vue';
import SongList from '@/components/SongList.vue';
import MyInput from '@/components/UI/MyInput.vue';
export default {
  components: { MyButton, SongList, MyInput},
  computed: {
      store() {
        return store
      }
    },
  data() {
    return {
      songs: [],
      musician: [],
      isFormAddText: false,
      song: [],
      str1: '',
      str2: '',
      file: null,
      files: [],

    };
  },
  mounted() {
    this.checkMusician();
    this.fetchFiles();
  },
  created() {
    this.getCurrentTheme();
  },
  methods: {
    async fetchFiles() {
      try {
        const response = await fetch('http://localhost:8000/list_files/');

        if (!response.ok) {
          const data = await response.json();
          console.log(data.message);
        } else {
          const data = await response.json();
          this.files = data.files;
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async toggleTheme() {
      store.dispatch('changeTheme');

      try {
        await axios.post('http://localhost:8000/set-theme/', {
          theme: store.getters.getTheme
        }, { withCredentials: true });
      } catch (error) {
        console.error('Ошибка при установке темы:', error);
      }

    },
    async getCurrentTheme() {

      try {
        const response = await axios.get('http://localhost:8000/get-theme/', {
          withCredentials: true  
        });

        if (response.data.theme === 'True') {
          store.dispatch('changeTheme', true);  // Устанавливаем темную тему
        } else {
          store.dispatch('changeTheme', false);  // Устанавливаем светлую тему
        }
      } catch (error) {
        console.error('Ошибка при получении текущей темы:', error);
      }

    },
    checkMusician() {
      axios.post('http://localhost:8000/getMusician/', {userid: store.getters.getUser.id})
      .then(res => {
        if (res.status === 200 && res.data.message === 'correct') {
          
          this.musician = res.data.musician;
          console.log(this.musician);
          this.getMusicianSongs();
          // store.dispatch('setUser', res.data.user);
        }
        else if (res.status === 200 && res.data.message === 'notfound'){
          console.log('Пользователь без музыкальной карты');
        }
        else if (res.status === 200 && res.data.message === 'badrequest'){
          console.log('неверный метод запроса');
        }
      })
    },
    getMusicianSongs() {
      axios.post('http://localhost:8000/getMusicianSongs/', {musid: this.musician.id})
      .then(res => {
        if (res.status === 200 && res.data.message === 'correct') {
          this.songs = res.data.songs;
          console.log(this.songs);
          // store.dispatch('setUser', res.data.user);
        }
        else if (res.status === 200 && res.data.message === 'notfound'){
          console.log('не найдено треков');
        }
        else if (res.status === 200 && res.data.message === 'badrequest'){
          console.log('неверный метод запроса');
        }
      })
    },
    addText(song) {
      this.isFormAddText = !this.isFormAddText;
      this.song = song;
    },
    async saveTextForm() {
      const formData = new FormData();
      formData.append('song', this.song.namesong);
      formData.append('str1', this.str1);
      formData.append('str2', this.str2);

      try {
        const response = await fetch('http://localhost:8000/saveTextForm/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const data = await response.json();
          console.error('Errors:', data.errors);
        } else {
          const data = await response.json();
          console.log(data.message);
          this.str1 = '';
          this.str2 = '';
          this.fetchFiles();
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async saveTextFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('song', this.song.namesong);

      try {
        const response = await fetch('http://localhost:8000/saveTextFile/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const data = await response.json();
          console.error('Error:', data.error);
        } else {
          const data = await response.json();
          console.log(data.message);
          this.fetchFiles();
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    onFileChange(event) {
      this.file = event.target.files[0];
    },
  }
}
</script>

<style>
.dark-theme {
  background-color: #333;
  color: #fff;
}
.light-theme {
  background-color: #fff;
  color: #000;
}

.addText {
  background: rgb(50, 50, 50);
  border: 1px solid #61f798;
  border-radius: 1em;
  width: 70%;
  height: 70%;
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
.addTextBackground {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8); 
  z-index: 999;
}
.addTextForm {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}
</style>