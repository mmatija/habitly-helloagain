import authApi from '@/api/auth';

const TOKEN_KEY = 'auth_token';

export default {
  namespaced: true,

  state: {
    token: localStorage.getItem(TOKEN_KEY) || null,
  },

  getters: {
    isAuthenticated: (state) => state.token !== null,
    token: (state) => state.token,
  },

  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem(TOKEN_KEY, token);
    },
    clearToken(state) {
      state.token = null;
      localStorage.removeItem(TOKEN_KEY);
    },
  },

  actions: {
    async login({ commit }, { username, password }) {
      const response = await authApi.login(username, password);
      commit('setToken', response.data.token);
    },
    logout({ commit }) {
      commit('clearToken');
    },
  },
};
