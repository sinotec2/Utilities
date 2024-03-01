import axios from 'axios';

const baseURL = 'http://200.200.32.195:3000';

const api = axios.create({
  baseURL,
  withCredentials: true,
});

export const login = async (event, username, password) => {
  event.preventDefault(); 
  console.log('Inside login function:', username, password);
  try {
    const response = await api.post('/api/login', { username, password });
    console.log('Afterlogin:', username, password);
    return response.data.message;
  } catch (error) {
    console.error('Login failed:', error);
    throw new Error('Login failed. Please check your credentials.');
  }
};
