import {createStore} from "vuex";

export default createStore({
    state: () => ({
        isAuth: false,
        formAuth: false
    }),
    getters: {
        getIsAuth(state){
            return state.isAuth
        },
        getFormAuth(state){
            return state.formAuth
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
        changeFormAuth(){
            this.state.formAuth= !this.state.formAuth
        },
        // changeIsAuthAdmin(){
        //     this.state.isAuthAdmin = !this.state.isAuthAdmin
        // },
        // createUser(user){
        //     this.state.user = user
        // }
    }
})