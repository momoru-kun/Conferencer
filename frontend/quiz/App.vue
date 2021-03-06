<template>
  <v-app>
    <v-main>
      <v-form v-model="formValid" class="form" ref="form" v-if="activeConference && !formSended">
        <div class="text-h5">{{ conferenceName }}</div>
        <div class="text-body-2" style="margin-right: 2px;">Запись на конференцию</div>
        <v-text-field 
          solo 
          dense
          label="Имя"
          :rules="nameRules"
          hide-details="auto"
          class = "text-field"
          v-model="name"
          required
        > </v-text-field>
        <v-text-field 
          solo 
          dense
          label="Фамилия"
          :rules="nameRules"
          hide-details="auto"
          class = "text-field"
          v-model="surname"
          required
        > </v-text-field>
        <v-text-field 
          solo 
          dense
          label="Отчество"
          :rules="nameRules"
          hide-details="auto"
          class = "text-field"
          v-model="middlename"
          required
        > </v-text-field>
        <v-text-field 
          solo 
          dense
          label="E-mail"
          :rules="emailRules"
          hide-details="auto"
          class = "text-field"
          v-model="email"
          required
        > </v-text-field>
        <v-text-field 
          solo 
          dense
          label="Город"
          :rules="nameRules"
          hide-details="auto"
          class = "text-field"
          v-model="city"
          required
        > </v-text-field>
        <v-text-field 
          solo 
          dense
          label="ВУЗ"
          :rules="nameRules"
          hide-details="auto"
          class = "text-field"
          v-model = "uni"
          required
        > </v-text-field>
        <v-text-field 
          solo 
          dense
          label="Направление"
          :rules="nameRules"
          hide-details="auto"
          class = "text-field"
          v-model="study"
          required
        > </v-text-field>
        <v-checkbox
          label="С докладом"
          color="#22303D"
          hide-details
          v-model = "topic"
        ></v-checkbox>
        <v-scroll-x-transition>
          <v-text-field 
            solo 
            dense
            label="Название доклада"
            :rules="nameRules"
            required
            hide-details="auto"
            class = "text-field"
            v-if="topic"
            transition ="slide-x-transition"
            v-model = "topicSubject"
          > </v-text-field>
        </v-scroll-x-transition>
        <v-btn @click="sendForm"> Записаться </v-btn>
      </v-form>
      <div class="form" v-else-if="!formSended && !activeConference">
        <div class="text-h5">{{ conferenceName }}</div>
        <div class="text-body-2" style="margin-right: 2px; margin-top: 8px;">Приносим свои извинения, но запись на конференцию закрыта.</div>
      </div>
      <div class="form" v-else-if="formSended && activeConference">
        <div class="text-h5">Спасибо!</div>
        <div class="text-body-2" style="margin-right: 2px; margin-top: 8px;">Заявка на участии в {{ conferenceName }} успешно отправлена!</div>
      </div>
    </v-main>
  </v-app>
</template>

<script>
const axios = require('axios');
export default {
  name: 'App',

  methods: {
    getConferenceInfo: function () {
      axios.post('/api/conference.get', {id: location.pathname.replace('/c_', '')}).then((response) => {
        let confData = response.data.response[0]
        console.log(confData);
        this.conferenceName = confData.name;
        this.activeConference = confData.status;
        console.log(this.formSended)
        console.log(this.activeConference)
      })
    },
    sendForm: function() {
      this.$refs.form.validate()
      if (this.formValid) {
        let params = {
          topic: this.topic, 
          name: this.name, 
          surname: this.surname,
          middlename: this.middlename,
          email: this.email,
          city: this.city,
          uni: this.uni,
          study: this.study,
          topicSubject: this.topicSubject,
          conferenceName: "",
        }

        axios.post("/api/member.add/", {conf_id: location.pathname.replace('/c_', ''), form: params}).then(response => {
          console.log("Sended! " + response.status)
          this.formSended = true
        }).catch(err => {
          console.log("Error! " + err.message)
        })
      }
    }
  },

  mounted: function () {
    this.getConferenceInfo()
  },

  data: () => ({
    formValid: true,
    topic: false,
    name: "",
    surname: "",
    middlename: "",
    email: "",
    city: "",
    uni: "",
    study: "",
    topicSubject: "",
    conferenceName: "",
    activeConference: true,
    formSended: false,
    nameRules: [
      value => !!value || 'Обязательное поле.'
    ],
    emailRules: [
      v => !!v || 'Обязательное поле',
      v => /.+@.+\..+/.test(v) || 'Не верно введён email'
    ]
  }),
};
</script>

<style>
html {
  overflow: hidden !important;
}
body {
  background-color: #8EC5FC;
  background-image: linear-gradient(62deg, #8EC5FC 0%, #E0C3FC 100%);
}
.theme--light.v-application {
  background: none !important;
}
.v-main, .v-main__wrap {
  align-items: center;
  justify-content: center;
}
.v-input {
  margin: 4px 4px 12px 4px !important;
}
.v-input--checkbox {
  margin-left: 8px !important;
}
.v-text-field__details {
  margin-bottom: 0 !important;
}
.v-btn {
  margin-left: 8px !important;
  box-shadow: 5px 5px 15px rgba(34,48,61,0.15) !important;
  border-radius: 8px !important;
  background-color: rgba(255, 239, 239, 0.25) !important;
}
.v-input.text-field .v-input__slot {
  box-shadow: 5px 5px 15px rgba(34,48,61,0.15) !important;
  border-radius: 8px !important;
  background-color: rgba(235, 229, 205, 0.25) !important;
  color: #FFFEFE !important;
  width: calc(100% - 16px) !important;
}
.v-label, input[type="text"] {
  color: #22303D !important;
}
.form {
  display: block;
  padding: 16px;
  justify-content: left;
  color: #22303D;
  border-radius: 8px;
  backdrop-filter: blur(5px);
  background: rgba(235, 229, 205, 0.25);
  width: 450px;
  height: fit-content;
  margin: auto;
  box-shadow: 5px 5px 15px rgba(34,48,61,0.15);
  border: solid 2px rgba(239, 229, 205, 0.2);
  transition: 0.3s;
}
@media screen and (max-width: 700px) {
  .form {
    width: 100%;
    height: 100% !important;
  }
  .v-main__wrap {
    height: 100% !important
  }
}
</style>