const axios = require('axios');
export default {
    state: {
        token: localStorage.getItem('token') || '',
        status: ''
    },
    mutations: {
        auth_request(state) {
            state.status = 'loading'
        },
        auth_success(state, token){
            state.status = 'success'
            state.token = token
        },
        auth_error(state){
            state.status = 'error'
        },
        logout(state){
            state.status = ''
            state.token = ''
        },
    },
    actions: {
        login(ctx, user) {
            return new Promise((resolve, reject) => {
                ctx.commit('auth_request')
            
            const promise = axios.post('/api/user.token.obtain', {username: user.login, password: user.password})
            
            promise.then((response) => {
                    if (response.status == 200) {
                        console.log(response.data)
                        
                        const token = response.data.token
                        localStorage.setItem('token', token)
                        axios.defaults.headers.common['Authorization'] = "Bearer " + token
                        ctx.commit('auth_success', token)
                        console.log('token')
                        resolve(response)
                }})
                .catch(err => {
                    ctx.commit('auth_error')
                    reject(err)
                })
            })
        },
        logout({commit}){
            return new Promise((resolve) => {
                commit('logout')
                localStorage.removeItem('token')
                delete axios.defaults.headers.common['Authorization']
                resolve()
            })
        }
    },
    getters: {
        token: state => state.token,
        user: state => state.user,
        isLoggedIn: state => !!state.token
    },
}