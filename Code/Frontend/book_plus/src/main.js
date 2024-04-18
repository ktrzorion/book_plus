import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import VueStarRating from 'vue-star-rating';
import store from './store';

const app = createApp(App);

app.config.globalProperties.$axios = axios;
app.config.globalProperties.$jwtDecode = jwtDecode;

app.component('star-rating', VueStarRating.default);

app.use(router);

app.use(store);

app.mount('#app');