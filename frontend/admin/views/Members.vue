<template>
    <div style="padding: 16px;">
        <div class="text-h6"> 
            {{ confName }} 
            <v-btn
                icon
                style="float: right"
                @click="exportMembers"
            >
                <v-icon> mdi-file-excel</v-icon>
            </v-btn>
        </div>
        <v-data-table 
            show-expand 
            single-expand 
            :headers="headers" 
            :items="members"
            :loading="loading"
            no-data-text = "Нет подавших заявку"
            style="transition: 0.3s"
            > 
            <template v-slot:item.name="{ item }">
                <v-chip style="width:100%" :color="getColor(item.approved)" v-if="item.approved != null"> {{ item.name }} </v-chip>
                <span v-else> {{ item.name }} </span>
            </template>
            <template v-slot:item.with_topic="{ item }">
                <v-icon> {{ item.with_topic ? "mdi-check" : "mdi-close" }} </v-icon>
            </template>
            <template v-slot:expanded-item="{ item }">
                <td style="padding: 8px; box-shadow: none;">
                    <div>
                        Email: <a :href="'mailto:' + item.email">{{ item.email }} </a> <br>
                        <span v-if="item.with_topic"> Тема доклада: {{ item.topic }} </span>
                    </div>
                </td>
                <td v-if="item.approved != null">
                    {{ item.approved ? 'Подтверждён' : 'Отклонён'}}
                </td>
                <td v-else>
                </td>
                <td style="padding-right: 4px;" v-if="item.approved === null">
                    <v-btn text color="secondary" @click="setApproval(item, true)" style="float:right"> Подтвердить </v-btn>
                </td>
                <td style="padding-left: 4px;" v-if="item.approved === null">
                    <v-btn text style="float:left;" @click="setApproval(item, false)"> Отклонить </v-btn>
                </td>
                <td>
                </td>
            </template>
        </v-data-table>
        <iframe id="downloadFrame" style="display:none"></iframe>
    </div>
</template>

<script>
const axios = require('axios');
export default {
    props: ['id'],
    data: () => ({
        confName: "",
        headers: [
            {text: 'ФИО', value: 'name', align: 'left'},
            {text: 'Город', value: 'city'},
            {text: 'Учебное заведение', value: 'uni'},
            {text: 'Направление', value: 'course'},
            {text: 'Выступает', value: 'with_topic', width: '50px'},
            {text: '', value: 'data-table-expand', width: '30px'},
        ],
        members: [],
        loading: true
    }),
    methods: {
        exportMembers: function () { 
            axios.get('/api/export.conferenceMembers?conf_id='+this.id, {headers: {Authorization: "Bearer " + this.getToken()}}).then((response) => {
                document.getElementById('downloadFrame').src = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + response.data.data
            })
        },
        getColor: (status) => {
            console.log(status)
            return status ? 'success' : 'error'
        },
        getToken: function () { return this.$store.getters.token },
        getConfirence: function() {
            axios.post('/api/conference.get', {'id': this.id}).then((response) => {
                this.confName = response.data.response[0].name
            })
        },
        getMembers: function() {
            axios.post(
                '/api/conference.members', 
                {conf_id: this.id},
                {headers: {Authorization: "Bearer " + this.getToken()}})
            .then((response) => {
                this.members = response.data.response
                this.loading = false
            })
        },
        setApproval: function (item, approval) { 
            axios.post(
                "/api/member.approve",
                {conf_id: this.id, member_id: item.id, approved: approval},
                {headers: {Authorization: "Bearer " + this.getToken()}}
                ).then(() => {
                    item.approved = approval
                })
        }
    },
    mounted: function() {
        this.getConfirence()
        this.getMembers()
    }
}
</script>

<style scoped>
.v-data-table__wrapper {
    margin: 0 i !important
}
</style>