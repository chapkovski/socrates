import Vue from 'vue'
import Vignette from './VignetteApp.vue'
import Vuex from 'vuex'
import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify'
import VueCookies from 'vue-cookies'
// index.js or main.js
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import store from './editor_store'
import router from './router'
import axios from 'axios'

Vue.prototype.$http = axios; //making axios globally available via http method
Vue.use(Vuetify)
Vue.use(Vuex);
Vue.use(VueCookies)

Vue.config.productionTip = false




new Vue({
  router,
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
  render: h => h(Vignette),
}).$mount('#app')
