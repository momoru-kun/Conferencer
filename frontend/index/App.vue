<template>
  <v-app id="app">
    <v-app-bar
      app
      color="rgba(50,50,50,0.25)"
      dark
      dense
      elevation="2"
    >
      <v-toolbar-title>Conferencer</v-toolbar-title>
  
      <v-spacer></v-spacer>
      <v-btn color="secondary" elevation="2" href="/admin"> Войти </v-btn>  
    </v-app-bar>
    <v-main app>
      <v-container
      fluid
      dark
      style="padding-top: 32px; height: 100%;"
      > 
      <v-row align="center" style="height: 100%">
        <v-col>
          <div class="text-h2"> Conferencer </div>
          <div class="text-subtitle-1" style="margin-left: 4px"> Управление участниками </div>
        </v-col>
      </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
};
</script>

<style>
html { 
  overflow-y: auto !important;
}
body, #app { 
  background-image: url("https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg");
  color: #ffffff;
  backdrop-filter: blur(10px);
}
</style>