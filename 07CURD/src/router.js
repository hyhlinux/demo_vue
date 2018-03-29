const routers = [{
    path: '/',
    meta: {
        title: ''
    },
    component: (resolve) => require(['./views/index.vue'], resolve)
},
{
    path: '/list',
    meta: {
        title: 'list message'
    },
    component: (resolve) => require(['./views/message2.vue'], resolve)
},
];
export default routers;