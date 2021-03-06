<template>
<v-container fill-height fluid>
  <v-row align="center" justify="center">
    <v-col>
      <v-card elevation="2" class="mx-auto" max-width="450">
        <v-card-title class="text-h5" style="background-color: #5428B3; color: white"> Регистрация </v-card-title>
        <v-card-text>
          <v-form class="loginForm" ref="form" v-model="validated"> 
            <v-text-field 
              class="padding"
              :rules="[rules.required, rules.minLogin]" 
              required 
              label="Логин"
              :error="loginNotUnique"
              :error-messages="loginNotUnique ? 'Выбранный логин занят' : ''"
              v-model="login"
              dense
              hide-details="auto"
              @change="checkLogin"
            > </v-text-field>
            <v-text-field 
              class="padding"
              dense
              :rules="[rules.required, rules.minPass]"
              required 
              hide-details="auto"
              label="Пароль" 
              :type="showPassword ? 'password' : 'text'" 
              v-model="password" 
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" 
              @click:append="showPassword = !showPassword"> </v-text-field>
            <v-text-field
              class="padding"
              dense
              hide-details="auto"
              :rules="[rules.required, rules.email]"
              type="email"
              label="Email адрес"
              v-model="email"
            > </v-text-field>
            <v-text-field
              class="padding"
              dense
              hide-details="auto"
              :rules="[rules.required]"
              label="Имя"
              v-model="name"
            > </v-text-field>
            <v-text-field
              class="padding"
              dense
              hide-details="auto"
              :rules="[rules.required]"
              label="Фамилия"
              v-model="surname"
            > </v-text-field>
            <v-btn color="secondary" @click="register" :loading="registerProcess"> Зарегистрироваться </v-btn>
          </v-form>
        </v-card-text>
        <v-divider> </v-divider>
        <v-card-actions dense align="end">
          <v-col dense align="end" style="padding: 0">
            <v-btn text color="#212121" :to="{name: 'Login'}"> Уже есть аккаунт </v-btn>
          </v-col>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<script>
const axios = require('axios');
export default {
  methods: {
    checkLogin: function () { 
      if (this.login < 5) {
        this.loginNotUnique = false
        return
      }
      axios.post('/api/user.check', {login: this.login}).then(() => {
        this.loginNotUnique = true
      }).catch(() => {
        this.loginNotUnique = false
      })
    },
    register: function () {
      this.$refs.form.validate()
      if (this.validated) {
        this.registerProcess = true
        let userData = {
          first_name: this.name,
          last_name: this.surname,
          email: this.email,
          login: this.login,
          password: this.password
        } 
        axios.post('/api/user.register', userData).then(((response) => {
          console.log(response)
          this.registerProcess = false
          this.$store.dispatch('show_notification', {type: 'success', text: 'Аккаунт успешно зарегистрирован'})
          this.$router.push('/login')
        }))
      } 
    }
  },
  data: () => ({
    login: "",
    loginNotUnique: false,
    password: "",
    passwordConfirmation: "",
    email: "",
    name: "",
    surname: "",
    showPassword: true,
    showPasswordConfirmation: true,
    registerProcess: false,
    rules: {
        required: value => !!value || 'Обязательное поле.',
        minLogin: v => v.length >= 5 || 'Минимум 5 символов',
        minPass: v => v.length >= 8 || 'Минимум 8 символов',
        email:  v => /.+@.+\..+/.test(v) || 'Не верно введён email'
    },
    validated: true
  }),
  mounted: function () {
    
  }
}
</script>

<style scoped>
.loginForm {
    padding: 8px 16px 8px 16px;
    width: 100%
}
.padding {
  padding-top: 8px;
  padding-bottom: 8px;
}
</style>