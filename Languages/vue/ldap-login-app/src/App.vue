<template>
  <div id="app" class="flex-container">
    <img alt="Vue logo" src="./assets/logo.png" class="logo">
    <router-view />
  </div>
</template>

<script>
import Login from "@/components/Login.vue";
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  data() {
    return {
      passwordReset: false, // 根据你的需求设置初始值
    };
  },
  name: 'App',
  components: {
    HelloWorld,
    Login,
  }
}
</script>

<style>
#	app {
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
