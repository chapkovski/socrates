import Vue from 'vue'
import Vuex from 'vuex'
import router from './router'
import axios from 'axios'
Vue.use(Vuex)
const store = new Vuex.Store({
    state: {
        saving: false,
    },
    getters: {
        savingStatus: (state) => state.saving,
    },
    mutations: {
        SAVING_INITIATED(state) {
            state.saving = true
        },
        SAVING_DONE(state) {
            state.saving = false
        },

    },
    actions: {
        savingRequested({ commit }) {
            console.debug('saving request initiated');
            commit('SAVING_INITIATED')

        },
        savingStopRequested({ commit }) {
            console.debug('saving STOP request initiated');
            commit('SAVING_DONE')
        },
        async deleteVignette({ commit }, vignette_id) {
            try {
                await axios.delete(`/api/vignettes/${vignette_id}/`);
                router.push({
                    name: "home",
                });
            }
            catch (error) {
                console.debug(error)
            }
        }
    }
})


export default store;  