import {createStore} from "vuex";

export default createStore({
    state: () => ({
        isAuth: false,
        formAuth: false,
        userData: [],
        theme: false,
        currentSong: [],
        token: '',
    }),
    getters: {
        getIsAuth(state){
            return state.isAuth
        },
        getFormAuth(state){
            return state.formAuth
        },
        getUser(state){
            return state.userData
        },
        getTheme(state) {
            return state.theme
        },
        getCurrentSong(state) {
            return state.currentSong
        },
        getToken(state){
            return state.token
        }
    },
    mutations: {
        set_User(state, user) {
            state.userData = user;
        },
        setTheme(state, theme) {
            state.theme = theme;
        },
        setCurrentSong(state, song) {
            state.currentSong = song;
        },
        set_Token(state, token) {
            state.token = token;
        }
    },
    actions: {
        changeIsAuth(){
            this.state.isAuth = !this.state.isAuth
        },
        changeFormAuth(){
            this.state.formAuth= !this.state.formAuth
        },
        setUser({commit}, user) {
            commit('set_User', user) 
        },
        setToken({commit}, token) {
            commit('set_Token', token) 
        },
        changeTheme({ commit }, theme = !this.state.theme) {
            commit('setTheme', theme);
        },
        changeSong({commit}, song) {
            commit('setCurrentSong', song);
        }
    }
})