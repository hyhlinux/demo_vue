import Index from './views/index.vue';
import Admin from './views/admin.vue';
import Home from './views/home.vue';
import Mail from './views/mail.vue';
import Login from './views/login.vue';
import Register from './views/register.vue';
import User from './views/user.vue';
import UserProfile from './views/user_profile.vue';
import UserProfileDef from './views/user_profile_def.vue';
const routers = [
    {
        path: '/',
        meta: {
            title: 'index',
            requiresAuth: true,
        },
        component: Index,
    },
    {
        path: '/home',
        meta: {
            title: 'home',
            requiresAuth: true,
        },
        component: Home,
    },
    {
        path: '/admin',
        meta: {
            title: 'admin',
            requiresAuth: true,
        },
        component: Admin,
    },
    // {
    //     path: '/user/:id',
    //     meta: {
    //         title: 'user'
    //     },
    //     component: User,
    //     children: [
    //         {
    //             path: '',
    //             component: UserProfileDef
    //         },
    //         {
    //             path: 'profile',
    //             component: UserProfile,
    //             children: [
    //                 {
    //                     path: 'mail',
    //                     component: Mail,
    //                 }
    //             ]
    //         }
    //     ]
    // },
    {
        path:'/user/:id/profile/mail',
        meta: {
            title: 'mail',
            requiresAuth: true,
        },
        component: Mail,
    },
    {
        path: '/login',
        meta: {
            title: 'login'
        },
        component: Login,
    },
    {
        path: '/register',
        meta: {
            title: 'register'
        },
        component: Register,
    },
];
export default routers;