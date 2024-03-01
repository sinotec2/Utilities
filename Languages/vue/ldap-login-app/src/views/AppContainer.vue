<!-- src/views/AppContainer.vue -->

<template>
  <div>
    <img alt="Vue logo" src="./src/assets/logo.png" class="logo">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <Login :passwordReset="passwordReset" />
    <router-view />
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */

import Login from "@/components/Login.vue";
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  data() {
    return {
      passwordReset: false,
    };
  },
  components: {
    HelloWorld,
    Login,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.flex-container { display: flex; }
.logo { width: 30px; height: 30px; margin-top: 30px; }
</style>

