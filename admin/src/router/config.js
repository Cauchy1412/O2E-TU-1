import TabsView from '@/layouts/tabs/TabsView'
import BlankView from '@/layouts/BlankView'
import PageView from '@/layouts/PageView'

// 路由配置
const options = {
    routes: [
        {
            path: '/login',
            name: '登录页',
            component: () => import('@/pages/login')
        },
        {
            path: '*',
            name: '404',
            component: () => import('@/pages/exception/404'),
        },
        {
            path: '/403',
            name: '403',
            component: () => import('@/pages/exception/403'),
        },
        {
            path: '/',
            name: '首页',
            component: TabsView,
            redirect: '/login',
            children: [
                {
                    path: 'dashboard',
                    name: '主面板',
                    meta: {
                        icon: 'dashboard',
                    },
                    component: () => import('@/pages/dashboard/analysis'),BlankView,
                    

                    // children: [
                    //     {
                    //         path: 'workplace',
                    //         name: '工作台',
                    //         meta: {
                    //             page: {
                    //                 closable: false
                    //             }
                    //         },
                    //         component: () => import('@/pages/dashboard/workplace'),
                    //     },
                    //     {
                    //         path: 'analysis',
                    //         name: '分析页',
                    //         component: () => import('@/pages/dashboard/analysis'),
                    //     },
                    //     {
                        
                    //         path: 'newPage',
                    //         name: '新页面',
                    //         component: () => import('@/pages/newPage'),
                    //     },
                        
                    // ]
                },
                
                {
                    path: 'user',
                    name: '用户管理',
                    meta: {
                        icon: 'form',
                        page: {
                            cacheAble: false
                        }
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'list',
                            name: '用户列表',
                            component: () => import('@/pages/form/advance/UserForm'),
                        },
                        
                        // {
                        //     path: 'new',
                        //     name: '新增用户',
                        //     component: () => import('@/pages/form/basic'),
                        // },
                        
                        
                    ]
                },
                // {
                //     path: 'list',
                //     name: '列表页',
                //     meta: {
                //         icon: 'table'
                //     },
                //     component: PageView,
                //     children: [
                //         {
                //             path: 'query',
                //             name: '文章列表1',
                //             meta: {
                //                 authority: 'queryForm',
                //             },
                //             component: () => import('@/pages/list/QueryList'),
                //         },
                //         /* 
                //         {
                //             path: 'primary',
                //             name: '标准列表',
                //             component: () => import('@/pages/list/StandardList'),
                //         },
                //         {
                //             path: 'card',
                //             name: '卡片列表',
                //             component: () => import('@/pages/list/CardList'),
                //         },
                //         {
                //             path: 'search',
                //             name: '搜索列表',
                //             component: () => import('@/pages/list/search/SearchLayout'),
                //             children: [
                //                 {
                //                     path: 'article',
                //                     name: '文章',
                //                     component: () => import('@/pages/list/search/ArticleList'),
                //                 },
                                
                //                 {
                //                     path: 'application',
                //                     name: '应用',
                //                     component: () => import('@/pages/list/search/ApplicationList'),
                //                 },
                //                 {
                //                     path: 'project',
                //                     name: '项目',
                //                     component: () => import('@/pages/list/search/ProjectList'),
                //                 }
                //             ]
                //         }*/
                //         {
                //             path: 'search',
                //             name: '文章列表2',
                //             component: () => import('@/pages/list/search/ArticleList'),
                //         },
                //         // {
                //         //     path: 'userTable',
                //         //     name: '用户列表',
                //         //     component: () => import('@/pages/userTable'),
                //         // },
                //         // {
                //         //     path: 'advance',
                //         //     name: '用户管理',
                //         //     component: () => import('@/pages/form/advance/UserForm'),
                //         // }

                //     ]
                // },
                
                {
                    path: 'interpretation',
                    name: '解读管理',
                    meta: {
                        icon: 'profile'
                    },
                    component: PageView,
                    children: [
                       /* {
                            path: 'basic',
                            name: '基础详情页',
                            component: () => import('@/pages/detail/BasicDetail')
                        },*/
                        {
                            path: 'list',
                            name: '解读列表',
                            component: () => import('@/pages/list/search/ArticleList'),
                        },
                        /*
                        {
                            path: 'advance',
                            name: '解读详情',
                            component: () => import('@/pages/detail/AdvancedDetail')
                        },
                        {
                            path: 'approval',
                            name: '解读审批',
                            component: () => import('@/pages/list/search/approval'),
                        },*/

                    ]
                },
                /*
                {
                    path: 'result',
                    name: '结果页',
                    meta: {
                        icon: 'check-circle-o',
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'success',
                            name: '成功',
                            component: () => import('@/pages/result/Success')
                        },
                        {
                            path: 'error',
                            name: '失败',
                            component: () => import('@/pages/result/Error')
                        }
                    ]
                },
                */
                /*
                {
                    path: 'exception',
                    name: '异常页',
                    meta: {
                        icon: 'warning',
                    },
                    component: BlankView,
                    children: [
                        {
                            path: '404',
                            name: 'Exp404',
                            component: () => import('@/pages/exception/404')
                        },
                        {
                            path: '403',
                            name: 'Exp403',
                            component: () => import('@/pages/exception/403')
                        },
                        {
                            path: '500',
                            name: 'Exp500',
                            component: () => import('@/pages/exception/500')
                        }
                    ]
                },
                {
                    path: 'components',
                    name: '内置组件',
                    meta: {
                        icon: 'appstore-o'
                    },
                    component: PageView,
                    children: [
                        {
                            path: 'taskCard',
                            name: '任务卡片',
                            component: () => import('@/pages/components/TaskCard')
                        },
                        {
                            path: 'palette',
                            name: '颜色复选框',
                            component: () => import('@/pages/components/Palette')
                        },
                        {
                            path: 'table',
                            name: '高级表格',
                            component: () => import('@/pages/components/table')
                        }
                    ]
                },
                {
                    name: '验权表单',
                    path: 'auth/form',
                    meta: {
                        icon: 'file-excel',
                        authority: {
                            permission: 'form'
                        }
                    },
                    component: () => import('@/pages/form/basic')
                },
                {
                    name: 'Ant Design Vue',
                    path: 'antdv',
                    meta: {
                        icon: 'ant-design',
                        link: 'https://www.antdv.com/docs/vue/introduce-cn/'
                    }
                },
                {
                    name: '使用文档',
                    path: 'document',
                    meta: {
                        icon: 'file-word',
                        link: 'https://iczer.gitee.io/vue-antd-admin-docs/'
                    }
                }*/
            ]
        },
    ]
}


export default options
