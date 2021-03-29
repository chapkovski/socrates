import Vue from 'vue'
import Vuex from 'vuex'
import _ from 'lodash'

Vue.use(Vuex)
const store = new Vuex.Store({
    state: {

        instructionsShow: false,
    },
    getters: {

    },
    mutations: {

        toggleInstructionsDialog: (state) => (state.instructionsShow = !state.instructionsShow),

    },
    actions: {


    }
})

export default store;  