import Index from './views/index.vue';
import Home from './views/home.vue';
import Admin from './views/admin.vue';
import Login from './views/login.vue';
import User from './views/user.vue';
import UserProfile from './views/user_profile.vue';

const routers = [
    {
        path: '/',
        meta: {
            title: ''
        },
        component: Index,
    },
    {
        path: '/home',
        meta: {
            title: 'home'
        },
        component: Home,
    },
    {
        path: '/admin',
        meta: {
            title: 'admin'
        },
        component: Admin,
    },
    {
        path: '/user/:id',
        meta: {
            title: 'user'
        },
        component: User,
        children: [
            {
                path: 'profile',
                component: UserProfile
            }
        ]
    },
    {
        path: '/login',
        meta: {
            title: 'login'
        },
        component: Login,
    },
];
export default routers;