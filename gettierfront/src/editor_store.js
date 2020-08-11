import Vue from 'vue'
import Vuex from 'vuex'
import router from './router'
import axios from 'axios'
Vue.use(Vuex)
const store = new Vuex.Store({
    state: {
        saving: false,
        bufferForNew: {},
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
        SET_BUFFER(state, payload) { 
            state.bufferForNew = payload
         },
        EMPTY_BUFFER(state) { state.bufferForNew = {} }

    },
    actions: {
        setBuffer({ commit }, vignette) {
            console.debug('IN SET BUFFER', vignette, "JOPA") 
            commit('SET_BUFFER', vignette            ) },
        emptyBuffer({ commit },) { commit('EMPTY_BUFFER') },
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