import Vue from 'vue'
import Vignette from './VignetteApp.vue'
import Vuex from 'vuex'
import 'material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import '@mdi/font/css/materialdesignicons.css'
import Vuetify from 'vuetify'

// index.js or main.js
import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader

import router from './router'
Vue.use(Vuetify)
Vue.use(Vuex);

Vue.config.productionTip = false




new Vue({
  router,
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
