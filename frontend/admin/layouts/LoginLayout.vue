<template>
<v-app>
    <v-main>
        <router-view> </router-view>
        <v-snackbar  
            color="success" 
            v-model="notification.show" 
            timeout="2000"> 
            {{ notification.text }} 
        </v-snackbar>
    </v-main>
</v-app>
</template>

<script>
import { mapGetters } from "vuex";
export default {
    name: 'LoginLayout',
    computed: mapGetters(['notification']),
}
</script>