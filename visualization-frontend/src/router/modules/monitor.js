/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const monitorRouter = {
  path: '/monitor',
  component: Layout,
  redirect: '/monitor/Mymonitor',
  name: 'Monitor',
  meta: {
    title: 'Monitor',
    icon: 'monitor'
  },
  children: [
    {
      path: 'Mymonitor',
      component: () => import('@/views/monitor/Mymonitor'),
      name: 'Mymonitor',
      meta: { title: 'Mymonitor' }
    },
    {
      path: 'Create-monitor',
      component: () => import('@/views/monitor/Createmonitor'),
      name: 'Createmonitor',
      meta: { title: 'Createmonitor' }
    }
  ]
}
export default monitorRouter
