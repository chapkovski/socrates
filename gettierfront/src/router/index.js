import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import SingleVignette from '@/components/Vignette'


Vue.use(Router)



export default new Router({
    mode: 'history',
    base: '/t',
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/vignette/:id',
            name: 'vignette',
            component: SingleVignette,
            props: true,
        },

    ]
})