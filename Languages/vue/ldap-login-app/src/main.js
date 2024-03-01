import { createApp } from 'vue'
import App from './App.vue'
import router from './router';
import FileUpload from './components/FileUpload.vue';

const app = createApp(App);
app.use(router);

if (process.env.NODE_ENV === 'development') {
  app.config.devtools = true;
  app.config.debug = true;
}

app.component('FileUpload', FileUpload);
app.mount('#app');
