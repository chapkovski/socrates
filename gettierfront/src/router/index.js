import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import SingleVignette from '@/components/Vignette'
import EditCreateVignette from '@/components/EditCreateVignette'
import ExtraBtns from '@/components/ExtraBtns'
import SaveTbr from '@/components/toolbars/SaveTbr.vue'
import EditDelete from '@/components/toolbars/EditDeleteTbr.vue'
import CreateTbr from '@/components/toolbars/CreateTbr.vue'



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
            path: '/view/vignette/:id',
            name: 'vignette',
             
            components: {
                default: SingleVignette,
                extrabtns: EditDelete
            },
            props: { default: true, extrabtns: true }
        },
        {
            path: '/create/vignette/',
            name: 'create_vignette',
            components: {
                default: EditCreateVignette,
                extrabtns: SaveTbr
            },
            props: { default: true, extrabtns: true }
        },
        {
            path: '/edit/vignette/:id',
            name: 'edit_vignette',
            components: {
                default: EditCreateVignette,
                extrabtns: SaveTbr
            },
            props: { default: true, extrabtns: true }
        },

    ]
})