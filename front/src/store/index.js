import {createStore} from "vuex";

export default createStore({
    state: () => ({
        isAuth: false,
        formAuth: false,
        userData: [],
        theme: false,
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
        }
    },
    mutations: {
        set_User(state, user) {
            state.userData = user;
        },
        setTheme(state, theme) {
            state.theme = theme;
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
        changeTheme({ commit }, theme = !this.state.theme) {
            commit('setTheme', theme);
        }
    }
})