import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify';
import store from './store'
import Axios from 'axios'

//import jwt_decode from 'jwt-decode'

Vue.config.productionTip = false
Vue.prototype.$http = Axios;

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
