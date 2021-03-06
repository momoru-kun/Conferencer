export default {
    actions: {
        show_notification({ commit }, notification) {
            return new Promise((resolve) => {
                commit('show_notification', notification)
                resolve(true)
            })
        }
    }, 
    mutations: {
        show_notification(state, notification)
        { 
            state.notification.type = notification.type;
            state.notification.color = notification.type;
            state.notification.text = notification.text;
            state.notification.show = true;

            setTimeout(() => {state.notification.show = false}, 3000)
        },
        close_notification(state) {
            state.notification.show.false
        }
    },
    state: {
        notification: {
            type: 'success',
            color: 'success',
            text: '',
            show: false
        }
    },
    getters: {
        notification: state => state.notification
    }
}