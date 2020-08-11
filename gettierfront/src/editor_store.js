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
            commit('SET_BUFFER', vignette)
        },
        emptyBuffer({ commit },) { commit('EMPTY_BUFFER') },
        savingRequested({ commit }) {
            commit('SAVING_INITIATED')
        },
        savingStopRequested({ commit }) {
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
        },
        async copyVignette({ commit }, vignette_id) {
            try {
                const resp = await axios.get(`/api/vignettes/${vignette_id}/`);
                commit('SET_BUFFER', resp.data);
                router.push({
                    name: "create_vignette",
                });
            }
            catch (error) {
                console.debug(error)
            }
        }
    }
})


export default store;  