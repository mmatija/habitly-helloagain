import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// Popper is required for bootstrap tooltips
import '@popperjs/core/dist/esm/popper';

const app = createApp(App).use(store).use(router);
app.mount('#app');
