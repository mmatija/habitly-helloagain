import axios from 'axios';
import config from '@/config';

const instance = axios.create({
  baseURL: config.apiUri,
  headers: {
    Accept: 'application/json',
  },
});

export default {
  login(username, password) {
    return instance.post('login/', { username, password });
  },
};
