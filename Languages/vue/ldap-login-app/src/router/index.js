
import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '@/components/HelloWorld.vue';
import Login from '@/components/Login.vue';
import FileUpload from '@/views/FileUpload.vue';
import AppContainer from '@/views/AppContainer.vue'; 

const routes = [
  {
    path: '/',
    name: 'AppContainer',
    component: AppContainer,
    children: [
      {
        path: '',
        name: 'HelloWorld',
        component: HelloWorld,
      },
      {
        path: 'login',
        name: 'Login',
        component: Login,
      },
      {
        path: 'file-upload',
        name: 'FileUpload',
        component: FileUpload,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

