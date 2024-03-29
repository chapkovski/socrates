import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex);
import axios from 'axios'

const store = new Vuex.Store({
    state: {
      vignette:null,
      chatExitAllowed: false,
      instructionsShow: false,
      errorDialog: !_.isEmpty(window.djangoErrors),
    },
    getters: {
      
    },
    mutations: {
        SET_VIGNETTE(state, payload) {
            state.vignette = payload
        },
        allowExitPermission: (state) => (state.chatExitAllowed = true),
        toggleInstructionsDialog: (state) => (state.instructionsShow = !state.instructionsShow),

        toggleErrorDialog: (state) => (state.errorDialog = !state.errorDialog),
    },
    actions: {
        async getVignette({ commit } ) {
            try {
                const path = window.path_to_vignette;
                await axios.get(path).then((response) => {
                    commit('SET_VIGNETTE', response.data);
                });
            }
            catch (error) {
                console.debug(error)
            }
        },
    }
})


export default store;  