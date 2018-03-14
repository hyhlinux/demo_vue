import Vue from 'vue';
import iView from 'iview';
import App from './App.vue';
import VueRouter from 'vue-router';
// import Routers from './router';

Vue.use(VueRouter);


const app = new Vue({
  el: '#app',
  router: Routers,
  render: h => h(App)
})
