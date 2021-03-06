<template>
<v-container fill-height fluid>
  <v-row align="center" justify="center">
    <v-col>
      <v-card elevation="2" class="mx-auto" max-width="450">
        <v-card-title class="text-h5" style="background-color: #5428B3; color: white"> Войти в Conferencer </v-card-title>
        <v-card-text>
          <v-form class="loginForm" ref="form" v-model="validated"> 
            <v-text-field :rules="Rules" required label="Логин" v-model="login"> </v-text-field>
            <v-text-field 
              :rules="Rules" 
              required 
              label="Пароль" 
              :type="showPassword ? 'password' : 'text'" 
              v-model="password" 
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" 
              @click:append="showPassword = !showPassword"> 
            </v-text-field>
            <v-alert dense outlined text color="red" type="error" v-if="authFail"> {{ ErrorText }} </v-alert>
            <v-btn color="secondary" @click="auth"> Войти </v-btn>
          </v-form>
        </v-card-text>
        <v-divider> </v-divider>
        <v-card-actions dense align="end">
          <v-col dense align="end" style="padding: 0">
            <v-btn text color="#212121" :to="{name: 'Register'}"> Регистрация </v-btn>
          </v-col>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
export default {
  data: () => ({
    login: "",
    password: "",
    validated: true,
    authFail: false,
    ErrorText: "",
    Rules: [
      value => !!value || 'Обязательное поле.'
    ],
    showPassword: true
  }),
  methods: {
    auth: async function() {
      this.$refs.form.validate();
      if (this.validated) {
        let login = this.login
        let password = this.password
        await this.$store.dispatch('login', { login, password })
        .then(() => {console.log('push'); this.$router.push('/')})
        .catch(err => {
          if (err.response) {
            if (err.response.data.non_field_errors[0] == "Unable to log in with provided credentials.") {
              this.authFail = true
              this.ErrorText = "Не верный логин/пароль"
            }
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.loginForm {
    padding: 8px 16px 8px 16px;
    width: 100%
}
</style>