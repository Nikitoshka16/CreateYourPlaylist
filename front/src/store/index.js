import {createStore} from "vuex";

export default createStore({
    state: () => ({
        isAuth: false,
    }),
    getters: {
        getIsAuth(state){
            return state.isAuth
        }
    },
    mutations: {
        // setClients(state, clients){
        //     state.clients = clients;
        // }
    },
    actions: {
        changeIsAuth(){
            this.state.isAuth = !this.state.isAuth
        },
        // changeIsAuthAdmin(){
        //     this.state.isAuthAdmin = !this.state.isAuthAdmin
        // },
        // createUser(user){
        //     this.state.user = user
        // }
    }
})