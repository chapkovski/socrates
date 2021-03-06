import Vue from 'vue'
import App from './App.vue'

import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify'

// index.js or main.js
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import axios from 'axios'

import store from './store'
import vueAwesomeCountdown from 'vue-awesome-countdown'

Vue.prototype.$http = axios; //making axios globally available via http method
Vue.use(Vuetify)
Vue.config.productionTip = false

Vue.use(vueAwesomeCountdown, 'vac') 


new Vue({
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
  render: h => h(App),
  store: store,
}).$mount('#app')
