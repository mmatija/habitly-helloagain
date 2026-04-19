import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';

import Home from '@/views/Home.vue';
import Login from '@/views/Login.vue';

const authGuard = (to, from, next) => {
  if (store.getters['auth/isAuthenticated']) {
    next();
  } else {
    next('/login');
  }
};

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: authGuard,
  },
  {
    path: '/habits',
    name: 'Habits',
    component: () =>
      import(/* webpackChunkName: "habits" */ '../views/Habits.vue'),
    beforeEnter: authGuard,
  },
  {
    path: '/habits/:id',
    name: 'HabitDetail',
    component: () =>
      import(/* webpackChunkName: "habits" */ '../views/HabitDetail.vue'),
    beforeEnter: authGuard,
  },
  {
    path: '/stacks',
    name: 'Stacks',
    component: () =>
      import(/* webpackChunkName: "stacks" */ '../views/Stacks.vue'),
    beforeEnter: authGuard,
  },
  {
    path: '/intentions',
    name: 'Intentions',
    component: () =>
      import(/* webpackChunkName: "stacks" */ '../views/Intentions.vue'),
    beforeEnter: authGuard,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
