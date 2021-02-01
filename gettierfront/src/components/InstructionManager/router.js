
import Vue from 'vue'
import Router from 'vue-router'
import Home from './Home'
import SingleInstruction from './Edit'




Vue.use(Router)



export default new Router({
    mode: 'history',
    base: '/instructions',
    routes: [
        {
            path: '/',
            name: 'home',
            components: {
                default:Home,
            }
        },
        {
            path: '/:id',
            name: 'single_instruction',
             
            components: {
                default: SingleInstruction,
                
            },
            props: { default: true,}
        },
      

    ]
})