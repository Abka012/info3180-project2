import { createRouter, createMemoryHistory } from 'vue-router'

export const createTestRouter = (options = {}) => {
  const {
    routes = [],
    initialRoute = '/'
  } = options

  const defaultRoutes = [
    { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
    { path: '/about', name: 'about', component: { template: '<div>About</div>' } },
    { path: '/register', name: 'register', component: { template: '<div>Register</div>' } },
    { path: '/login', name: 'login', component: { template: '<div>Login</div>' } },
    { path: '/profile', name: 'profile', component: { template: '<div>Profile</div>' } },
    { path: '/profile/edit', name: 'editProfile', component: { template: '<div>Edit Profile</div>' } },
    { path: '/browse', name: 'browse', component: { template: '<div>Browse</div>' } },
    { path: '/matches', name: 'matches', component: { template: '<div>Matches</div>' } },
    { path: '/messages', name: 'messages', component: { template: '<div>Messages</div>' } },
    { path: '/search', name: 'search', component: { template: '<div>Search</div>' } },
    { path: '/favorites', name: 'favorites', component: { template: '<div>Favorites</div>' } },
    { path: '/notifications', name: 'notifications', component: { template: '<div>Notifications</div>' } },
    { path: '/settings', name: 'settings', component: { template: '<div>Settings</div>' } }
  ]

  const mergedRoutes = routes.length > 0 
    ? routes 
    : defaultRoutes

  const router = createRouter({
    history: createMemoryHistory(),
    routes: mergedRoutes
  })

  if (initialRoute !== '/') {
    router.push(initialRoute)
  }

  return router
}

export const routerLinkStub = {
  template: '<a :href="to" @click.prevent="() => {}"><slot /></a>',
  props: ['to'],
  setup(props, { slots }) {
    return () => slots.default?.()
  }
}

export const createRouterWithParams = (params = {}) => {
  const routes = []
  
  for (const [path, name] of Object.entries(params)) {
    routes.push({
      path,
      name,
      component: { template: `<div>${name}</div>` }
    })
  }
  
  return createTestRouter({ routes })
}
