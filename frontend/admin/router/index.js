import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Members from '../views/Members.vue'
import AllMembers from '../views/AllMembers.vue'
import Register from '../views/Register'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      layout: 'login-layout'
    }
  },
  {
    path: '/conference/:id',
    component: Members,
    name: 'Conference',
    meta: {
      requiresAuth: true
    },
    props: true
  },
  {
    path: '/register',
    component: Register,
    name: 'Register',
    meta: {
      layout: 'login-layout'
    }
  },
  {
    path: '/members',
    component: AllMembers,
    name: 'Members',
    meta: {
      requiresAuth: true
    },
    props: true
  }
]

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/login') 
  } else {
    next() 
  }
})

export default router
