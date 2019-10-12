import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/* Router Modules */
/*
import componentsRouter from './modules/components'
import chartsRouter from './modules/charts'
import tableRouter from './modules/table'
import nestedRouter from './modules/nested'
import monitorRouter from './modules/monitor'
*/
/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  
  {
    path: '',
    component: Layout,
    redirect: 'dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: 'dashboard', icon: 'dashboard', noCache: true, affix: true }
      }
    ]
  },

  {
    path: '/monitor',
    component: Layout,
    redirect: '/monitor/index',
    children: [
      {
        path: 'index',
        component: () => import('@/views/monitor/index'),
        name: 'monitor',
        meta: { title: 'Monitor', icon: 'monitor', noCache: true }
      }
    ]
  },

  {
    path: '/Trans_cis',
    component: Layout,
    redirect: '/顺反式校验',
    children: [
      {
        path: 'trans_cis',
        component: () => import('@/views/visualization/trans_cis/index'),
        name: 'trans_cis',
        meta: { title: 'Trans_cis', icon: 'visualization' }
      }
    ]
  },
  {
    path: '/AsyncQueueMonitor',
    component: Layout,
    redirect: '/Async',
    children: [{
      path: 'Async',
      component: () => import('@/views/AsyncMonitor'),
      name: 'AsyncMonitor',
      meta: { title: 'AsyncMonitor', icon: 'tree' }
    }]
  }
/*
  {
    path: '/visualization',
    component: Layout,
    redirect: '/visualization/mutation',
    name: 'visualization',
    meta: {
      title: 'MutationVisual',
      icon: 'visualization'
    },
    children: [
      {
        path: 'trans_cis',
        component: () => import('@/views/visualization/trans_cis/index'),
        name: 'trans_cis',
        meta: { title: 'trans_cis' }
      },
      {
        path: 'mutation',
        component: () => import('@/views/visualization/mutation/index'),
        name: 'mutation',
        meta: { title: 'mutation' }
      }// component: () => import('@views/excel/select-excel'), name: 'selectExcel', meta: { title: 'selectExcel' }},
      //, component: () => import('@views/excel/upload-excel'), name: 'uploadExcel', meta: { title: 'uploadExcel' }}
    ]
  }*/
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
