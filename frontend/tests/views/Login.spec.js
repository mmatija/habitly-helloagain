import { mount, flushPromises } from '@vue/test-utils';
import { createStore } from 'vuex';
import { createRouter, createMemoryHistory } from 'vue-router';
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import authModule from '@/store/modules/auth';
import Login from '@/views/Login.vue';

const server = setupServer(
  rest.post('http://localhost/api/login/', (req, res, ctx) =>
    res(ctx.json({ token: 'test-token' })),
  ),
);
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function makeStore() {
  return createStore({ modules: { auth: authModule } });
}

function makeRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: { template: '<div>Home</div>' } },
      { path: '/login', component: Login },
    ],
  });
}

async function mountLogin() {
  const store = makeStore();
  const router = makeRouter();
  await router.push('/login');
  const wrapper = mount(Login, { global: { plugins: [store, router] } });
  return { wrapper, router };
}

describe('Login.vue', () => {
  it('redirects to / after successful login', async () => {
    const { wrapper, router } = await mountLogin();
    await wrapper.find('#username').setValue('alice');
    await wrapper.find('#password').setValue('secret');
    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(router.currentRoute.value.path).toBe('/');
  });

  it('shows a loading indicator while login is in progress', async () => {
    const { wrapper } = await mountLogin();
    await wrapper.find('#username').setValue('alice');
    await wrapper.find('#password').setValue('secret');
    await wrapper.find('form').trigger('submit');

    expect(wrapper.find('button[type="submit"]').text()).toBe('Logging in…');
  });

  it('shows an error message when credentials are invalid', async () => {
    server.use(
      rest.post('http://localhost/api/login/', (req, res, ctx) =>
        res(ctx.status(401), ctx.json({ error: 'Invalid credentials' })),
      ),
    );

    const { wrapper } = await mountLogin();
    await wrapper.find('#username').setValue('alice');
    await wrapper.find('#password').setValue('wrongpassword');
    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(wrapper.text()).toContain('Invalid username or password');
  });

  it('disables the submit button when username is empty', async () => {
    const { wrapper } = await mountLogin();
    const button = wrapper.find('button[type="submit"]');

    await wrapper.find('#password').setValue('secret');
    expect(button.element.disabled).toBe(true);

  });

  it('disables the submit button when password is empty', async () => {
    const { wrapper } = await mountLogin();
    const button = wrapper.find('button[type="submit"]');

    await wrapper.find('#username').setValue('alice');
    expect(button.element.disabled).toBe(true);
  });
});
