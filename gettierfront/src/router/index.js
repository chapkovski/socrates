import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import SingleVignette from '@/components/Vignette'
import CreateVignette from '@/components/CreateVignette'


Vue.use(Router)



export default new Router({
    mode: 'history',
    base: '/vignettemanager',
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
        {
            path: '/create/vignette/',
            name: 'create_vignette',
            component: CreateVignette,
        },

    ]
})