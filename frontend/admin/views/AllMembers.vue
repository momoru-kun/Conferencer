<template>
    <div style="padding: 16px;">
        <div class="text-h6"> 
            Все участники
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
            loading-text = "Идёт загрузка данных..."
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
                    <v-btn text color="secondary" :loading="item.approving" @click="setApproval(item, true)" style="float:right"> Подтвердить </v-btn>
                </td>
                <td style="padding-left: 4px;" v-if="item.approved === null">
                    <v-btn text style="float:left;" :loading="item.approving" @click="setApproval(item, false)"> Отклонить </v-btn>
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
    data: () => ({
        confName: "",
        headers: [
            {text: 'ФИО', value: 'name', align: 'left'},
            {text: 'Город', value: 'city'},
            {text: 'Учебное заведение', value: 'uni'},
            {text: 'Направление', value: 'course'},
            {text: 'Выступает', value: 'with_topic', width: '50px'},
            {text: 'Конференция', value: 'conf_name'},
            {text: '', value: 'data-table-expand', width: '30px'},
        ],
        members: [],
        loading: true
    }),
    methods: {
        exportMembers: function () { 
            axios.get('/api/export.allMembers', {headers: {Authorization: "Bearer " + this.getToken()}}).then((response) => {
                document.getElementById('downloadFrame').src = 'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,' + response.data.data
            })
        },
        getColor: (status) => {
            console.log(status)
            return status ? 'success' : 'error'
        },
        getToken: function () { return this.$store.getters.token },
        getAllMembers: function() {
            axios.post('/api/member.all', {}, {headers: {Authorization: "Bearer " + this.getToken()}}).then((response) => {
                console.log(response.data)
                this.members = response.data.response
                this.members.forEach((member) => member.approving = false) 
                this.loading = false
            })
        },
        setApproval: function (item, approval) { 
            item.approving = true
            axios.post(
                "/api/member.approve",
                {conf_id: item.conf_id, member_id: item.id, approved: approval},
                {headers: {Authorization: "Bearer " + this.getToken()}}
                ).then(() => {
                    item.approving = false
                    item.approved = approval
                })
        }
    },
    mounted: function() {
        this.getAllMembers()
    }
}
</script>

<style scoped>
.v-data-table__wrapper {
    margin: 0 i !important
}
</style>