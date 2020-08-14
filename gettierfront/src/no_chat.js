import Vue from 'vue'
import NoChatVignette from './NoChatVignette.vue'
import Vuex from 'vuex'
import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify'
import VueCookies from 'vue-cookies'
// index.js or main.js
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

import store from './store'

import axios from 'axios'

Vue.prototype.$http = axios; //making axios globally available via http method
Vue.use(Vuetify)
Vue.use(Vuex);
Vue.use(VueCookies)

Vue.config.productionTip = false




new Vue({
  store,
  vuetify: new Vuetify(
    {
      defaultAssets: {
        font: true,
        icons: 'mdi'
      },
      icons: {
        iconfont: 'mdi',
      }
    }
  )
  ,
  render: h => h(NoChatVignette),
}).$mount('#app')
