import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./views/G6.vue')
    },
    {
      path: '/g6',
      name: 'g6',
      component: () => import('./views/G6.vue')
    },
    {
      path: '/pnl',
      name: 'pnl',
      component: () => import('./views/PNL.vue')
    },
    {
      path: '/dbUpload',
      name: 'dbUpload',
      component: () => import('./views/dbUpload.vue')
    },
    {
      path: '/params',
      name: 'params',
      component: () => import('./views/params.vue')
    },
    {
      path: '/allocation',
      name: 'allocation',
      component: () => import('./views/allocations.vue')
    },
    {
      path: '/securities',
      name: 'securities',
      component: () => import('./views/securities.vue')
    },
    {
      path: '/histRanks',
      name: 'histRanks',
      component: () => import('./views/histRanks.vue')
    },
    {
      path: '/stratA',
      name: 'stratA',
      component: () => import('./views/strat_A.vue')
    },
    {
      path: '/stratB',
      name: 'stratB',
      component: () => import('./views/strat_B.vue')
    },
    {
      path: '/stratC',
      name: 'stratC',
      component: () => import('./views/strat_C.vue')
    }
  ]
})


