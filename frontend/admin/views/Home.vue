<template>
  <div style="padding: 16px">
    <div class="text-h4">      
      Конференции 
      <v-btn
        icon
        style="float: right"
        @click="exportConferences"
      >
        <v-icon> mdi-file-excel</v-icon>
      </v-btn>
    </div>

    <v-data-table
      :headers = "headers"
      :items = "conferences"
      no-data-text="Нет конференций. Чтобы создать, нажмите '+' в правом нижнем углу"
    >
    <template v-slot:item.active="{ item }" >
      <v-btn rounded small :color="getColor(item.active)" @click="changeConferenceStatus(item)">
        <span style="width: 100%; float: right;">{{ item.active ? "Открыта" : "Закрыта" }}</span>
      </v-btn>
    </template>
    <template v-slot:item.edit="{ item }">
      <v-menu
        top
        style="display: inline"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
            style="display: inline"
          >
            <v-icon> mdi-dots-vertical </v-icon>
          </v-btn>
        </template>
  
        <v-list dense>
          <v-list-item @click="getLink(item.id)">
            <v-list-item-icon> <v-icon> mdi-link </v-icon> </v-list-item-icon>
            <v-list-item-title>Ссылка на форму</v-list-item-title>
          </v-list-item>
          <v-list-item :to="{name: 'Conference', params: {id: item.id}}">
            <v-list-item-icon> <v-icon> mdi-human-queue </v-icon> </v-list-item-icon>
            <v-list-item-title> Участники </v-list-item-title>
          </v-list-item>
          <v-list-item @click="deleteConference(item)">
            <v-list-item-icon> <v-icon> mdi-delete </v-icon> </v-list-item-icon>
            <v-list-item-title>Удалить</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </template>
    </v-data-table>
    <v-btn 
      color="secondary"
      elevation="2"
      large
      fab
      style="position: fixed; bottom: 25px; right: 25px; font-size: 48px;"
      @click="newConfDialog = !newConfDialog"
    > <v-icon> mdi-plus </v-icon> </v-btn>
    <v-dialog
      v-model="newConfDialog"
      max-width="500px"
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar elevation="2" color="primary" dark> <div class="text-h6">Создать конференцию</div> </v-toolbar>
        <v-card-actions>
          <v-form v-model="addConfFormValid" style="width: 100%" ref="form">
            <v-text-field 
              :rules="Rules"
              required
              hide-details="auto" 
              v-model="newConfName"
              label="Название конференции"></v-text-field>
            <v-btn
              text
              :loading = "addConfLoading"
              :disabled = "addConfLoading"
              color="secondary"
              style="margin-top: 8px; float: right"
              @click="insertConference"
            >
              Создать
            </v-btn>
          </v-form>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="confLinkDialog"
      max-width="500px"
      transition="dialog-bottom-transition"
    > 
      <v-card>
        <v-toolbar elevation="2" color="primary" dense dark> <div class="text-h6">Ссылка на форму-приглашение</div> </v-toolbar>
        <v-card-text> 
          <v-text-field 
              :rules="Rules"
              required
              hide-details="auto" 
              v-model="confLink"
              disabled
              ></v-text-field>
          <div class="text-small"> Ссылка доступна всегда, пока запись на конференцию открыта</div>
        </v-card-text>
        <v-card-actions>
          <v-btn text color="secondary" style="float:right;" @click="copyLinkToClipboard"> Скопировать </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar color="success" text v-model="snackbar" timeout="2000"> 
      {{ snackbarText }} 
      <v-btn
        color="secondary"
        text
        @click="snackbar = false"
      >
        Close
      </v-btn>
    </v-snackbar>
  <iframe id="downloadFrame" style="display:none"></iframe>
  </div>
</template>

<script>
const axios = require('axios');
import { mapGetters } from "vuex";
export default {
  name: 'Home',
  computed: mapGetters(['token']),
  methods: {
    exportConferences: function () { 
      axios.get('/api/export.conferences', {headers: {Authorization: "Bearer " + this.getToken()}}).then((response) => {
        console.log(response.data.data)
        document.getElementById('downloadFrame').src = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + response.data.data
      })
    },
    changeConferenceStatus: function(item) {
      axios.post(
        '/api/conference.activity', 
        {conf_id: item.id},
        {headers: {Authorization: "Bearer " + this.getToken()}})
        .then(() => {
          item.active = !item.active;
          this.showSnackbar("Статус записи изменён!")
        })
    },
    deleteConference: function(item) { 
      axios.post(
          '/api/conference.delete', 
          {conf_id: item.id},
          {headers: {Authorization: "Bearer " + this.getToken()}})
          .then(() => {
            this.conferences.splice(this.conferences.indexOf(item))
            this.showSnackbar("Удалено успешно!")
          })
    },
    copyLinkToClipboard: function() { 
      navigator.clipboard.writeText(this.confLink).then(() => {
        this.showSnackbar("Ссылка скопирована в буфер обмена")
      })
      
    },
    showSnackbar: function(text) {
      this.snackbarText = text;
      this.snackbar = true
    },
    getLink: function (item) {
      console.log(location.path)
      console.log(item)
      let port = window.location.port == "80" || window.location.port == "443" ? "" : ":" + window.location.port
      this.confLink = window.location.protocol + "//" + window.location.hostname + port + "/c_" + item 
      this.confLinkDialog = true
    },
    getColor: (status) => (status ? 'success' : 'error'),
    getToken: function () { return this.$store.getters.token },
    insertConference:  function () {
      this.$refs.form.validate()
      if (this.addConfFormValid) {
        this.addConfLoading = true
        axios.post(
          '/api/conference.add', 
          {name: this.newConfName},
          {headers: {Authorization: "Bearer " + this.getToken()}})
          .then((response) => {
            this.addConfLoading = false; 
            setTimeout(() => {this.newConfDialog = false}, 500);
            this.conferences.push({id: response.data.conference_id, name: this.newConfName, active: true, edit: ''})
          })
      }
    }
  },
  mounted: function () {
    axios.post(
      '/api/conference.all', {},
      {headers: {Authorization: "Bearer " + this.getToken()}})
    .then((response) => {
      this.tableLoading = false
      const resp = response.data.response
      resp.forEach(elem => {elem.edit = ''})
      this.conferences = response.data.response 
    })
  },
  data: () => ({
    newConfDialog: false,
    newConfName: "",
    Rules: [value => !!value || 'Обязательное поле.'],
    addConfLoading: false,
    addConfFormValid: true,
    headers: [
      {text: 'Название', value: 'name', aling: 'left'},
      {text: 'Подали заявку', value: 'count', align: 'center'},
      {text: 'Запись', value: 'active', align: 'right', width: '150px'},
      {text: '', value: 'edit', sortable: false, width: '30px'}
    ],
    tableLoading: true,
    conferences: [],
    confLink: '',
    confLinkDialog: false, 
    snackbar: false, 
    snackbarText: ""
  })
}
</script>
