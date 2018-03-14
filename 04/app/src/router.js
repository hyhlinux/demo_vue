import Vue from 'vue';
import VueRouter from 'vue-router';
import home from './component/home.vue';


const routers = [
    {
        path: '/home', 
        name:'home', 
        component: home
    }
]


export default new VueRouter({
    routers
})