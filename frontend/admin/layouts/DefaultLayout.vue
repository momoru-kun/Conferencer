<template>
<v-app>
    <v-app-bar app collapse collapse-on-scroll color="primary" dense dark v-if="this.$route.name != 'Login'">
        <v-app-bar-nav-icon @click="drawer = true"></v-app-bar-nav-icon>
        <v-toolbar-title>Conferencer</v-toolbar-title>
    </v-app-bar>
    <v-navigation-drawer
        v-model="drawer"
        absolute
        temporary
        v-if="this.$route.name != 'Login'"
        >
        <v-list dense>
            <v-list-item link>
                <v-list-item-content>
                    <v-list-item-title class="title"> {{ user.username }}</v-list-item-title>
                    <v-list-item-subtitle> {{ user.email }} </v-list-item-subtitle>
                    <v-btn block color="secondary" style="margin-top:12px" @click="logout"> Выйти </v-btn>
                </v-list-item-content>
            </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list nav dense>
            <v-list-item link :to="{name: 'Home'}">
                <v-list-item-icon>
                    <v-icon>mdi-human-capacity-increase</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Все Конференции</v-list-item-title>
            </v-list-item>
            <v-list-item link :to="{name: 'Members'}">
                <v-list-item-icon>
                    <v-icon>mdi-human-queue</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Все участники</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
    <v-main> 
        <router-view> </router-view>
    </v-main>
</v-app>
</template>

<script>
export default {
    name: 'DefaultLayout'
}
</script>

<script>
import axios from 'axios';
import { mapGetters } from "vuex";
export default {
    name: 'App',
    computed: mapGetters(['token']),
    methods: {
        getUserData: function() {
            axios.get('/api/user.get', {headers: {Authorization: 'Bearer ' + this.getToken()}}).then((response) => {
                console.log(response.data)
                this.user = response.data
            }).catch((err) => {
                if (err.response.status == 401) {
                    this.$store.dispatch('logout').then(() => {
                        this.$router.push('/login')
                    })
                }
            })
        },
        getToken: function () { return this.$store.getters.token },
        logout: function () { 
            this.$store.dispatch('logout').then(() => { 
                this.$router.push('/login') 
            })
        }
    },
    mounted: function() {
        this.getUserData()
    },
    data: () => ({
        drawer: false,
        user: {}
    }),
};
</script>

<style>
html {
    overflow-y: auto !important;
}
</style>