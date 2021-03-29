import Vue from 'vue'
import NoChatVignette from './EssayApp.vue'
import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify'


import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import axios from 'axios'

Vue.prototype.$http = axios; //making axios globally available via http method
import store from './store'
Vue.use(Vuetify)

import vueAwesomeCountdown from 'vue-awesome-countdown'
Vue.use(vueAwesomeCountdown, 'vac') 


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
