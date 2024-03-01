<template>
  <div>
    <h2>LDAP Login</h2>
    <form @submit.prevent="event => login(event, username, password)" v-if="!passwordReset">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" required>
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" :disabled="!username" required>
      <button type="submit" :disabled="!username || !password">Login</button>
      <p><a @click="showPasswordReset">Forgot Password?</a></p>
    </form>
    <form @submit.prevent="resetPassword" v-if="passwordReset">
      <label for="resetEmail">Enter your email:</label>
      <input type="email" id="resetEmail" v-model="resetEmail" required>
      <button type="submit" :disabled="!resetEmail">Reset Password</button>
      <p><a @click="cancelPasswordReset">Cancel</a></p>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
    <form @submit.prevent="handleLogin" v-if="!passwordReset">
      <button type="submit" :disabled="!username || !password">Login</button>
    </form>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>



<script>
export default {
  data() {
    return {
    username: '',
    password: '',
    error: '',
      resetEmail: '',
      passwordReset: false,
    };
  },
  methods: {
    showPasswordReset() {
      this.passwordReset = true;
      this.error = '';
    },
    cancelPasswordReset() {
      this.passwordReset = false;
      this.resetEmail = '';
      this.error = '';
    },
    async resetPassword() {
      try {
        // 处理后端响应，可能需要显示成功消息或执行其他操作
        console.log(response.data.message);

        this.passwordReset = false;
        this.resetEmail = '';
      } catch (error) {
        this.error = 'Password reset failed. Please try again.';
      }
    }
  }
};
</script>

<script setup>
import { ref } from 'vue';
import { login } from '@/api';

const username = ref('');
const password = ref('');
const error = ref('');

const handleLogin = async () => {
  console.log('Entering handleLogin');
  console.log('Before login:', username.value, password.value);
  try {
    const response = await login(username.value, password.value);
    console.log(response);
    this.$store.commit('setUser', response.user);
  } catch (error) {
    if (error.message.includes('401')) {
      error.value = 'Invalid username or password. Please try again.';
    } else {
      error.value = 'An error occurred during login. Please try again later.';
    }
  }
};
</script>
<style scoped>
/* 样式可以根据需要进行自定义 */
h2 {
  text-align: center;
}

form {
  max-width: 300px;
  margin: 100px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>

