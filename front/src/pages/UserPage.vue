<template>
  <div>
    <my-button 
    @click="toggleTheme"
    >
    {{ store.getters.getTheme == false ? 'Switch to MORE DARK Theme' : 'Switch to Dark Theme' }}
    </my-button>
  </div>
</template>

<script>
import axios from 'axios';
import store from '@/store';
import MyButton from '../components/UI/MyButton.vue';
export default {
  components: { MyButton },
  computed: {
      store() {
        return store
      }
    },
  data() {
    return {
      
    };
  },
  created() {
    this.getCurrentTheme();
  },
  methods: {
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

        console.log(response);
        if (response.data.theme === 'True') {
          store.dispatch('changeTheme', true);  // Устанавливаем темную тему
        } else {
          store.dispatch('changeTheme', false);  // Устанавливаем светлую тему
        }
      } catch (error) {
        console.error('Ошибка при получении текущей темы:', error);
      }

    }
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
</style>