import { createRouter, createWebHashHistory } from 'vue-router'


const routes = [
    {
        path: "/",
        name: "price",
        component: require('../views/latestPrice.vue').default,

    },
];

const router = createRouter({
    routes,
    history: createWebHashHistory(),
});


// router.beforeEach((to, from, next) => {
//     // 假设有一个判断用户是否登录的方法，比如 isAuthenticated
//     if (to.path !== '/login' && localStorage.getItem("token") === null) {
//       next('/login'); // 如果未登录，重定向到登录页
//     } 
//     else {
//       next();
//     }
//   })

export default router;