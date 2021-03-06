import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                primary: '#5428B3',
                secondary: '#F70B7E',
                error: "#B00020"
            }
        }
    }
});
