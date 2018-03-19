import Vue from 'vue';
import iView from 'iview';
import VueRouter from 'vue-router';
import Routers from './router';
import Util from './libs/util';
import App from './app.vue';
import 'iview/dist/styles/iview.css';


Vue.use(VueRouter);
Vue.use(iView);


// 路由配置
const RouterConfig = {
    mode: 'history',
    routes: Routers
};
const router = new VueRouter(RouterConfig);

router.beforeEach((to, from, next) => {
    iView.LoadingBar.start();
    Util.title(to.meta.title);
    let token = window.localStorage.getItem('token');
    // API ser: 设定的时间，为未来的过期时间点
    let expires = parseInt(window.localStorage.getItem('expires')) || 0;  
    let curTime = new Date().getTime();
    if (to.matched.some(record => record.meta.requiresAuth) && (!token || token === null || curTime > expires))  {
        //该路由需要token
        // token 是否过期
        console.log(curTime, expires);
        window.localStorage.removeItem("token");
        window.localStorage.removeItem("expires");
        next({
            path: '/login',
            query: { redirect: to.fullPath }
        });
    } else {
        next();
    }
});

router.afterEach(() => {
    iView.LoadingBar.finish();
    window.scrollTo(0, 0);
});



new Vue({
    el: '#app',
    router: router,
    render: h => h(App)
});