import {createRouter, createWebHistory} from 'vue-router';
import MainPage from '@/pages/MainPage.vue';
import PlaylistPage from '@/pages/PlaylistPage.vue';
import UserPage from '@/pages/UserPage.vue';

import store from '@/store/index.js';


const routes = [
    {
        path: '/',
        name: 'mainPage',
        component: MainPage
    },
    {
        path: '/profile/:id?',
        name: 'userPage',
        component: UserPage
    },
    {
        path: '/playlist/:id?',
        name: 'playlistPage',
        component: PlaylistPage
    }
]

const router = createRouter({
    routes,
    history: createWebHistory(import.meta.env.BASE_URL)
})

router.beforeEach(async (to) => {
    if (!store.getters.getIsAuth && to.name !== 'mainPage')
    {
        return [{name : 'playlistPage'},
                {name : 'userPage'}]
    }

})

export default router;