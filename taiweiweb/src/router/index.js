import {createRouter, createWebHistory} from 'vue-router'

// 路由列表
const routes = [
    {
        meta: {
            title: "汇总数据",
            keepAlive: true
        },
        path: '/',         // uri访问地址
        name: "Home",
        component: () => import("../views/Home.vue")
    },
    {
        meta: {
            title: "订单详情",
            keepAlive: true
        },
        path: "/UserInfo/:name/:success/:back/:wait/:search_date",         // uri访问地址
        name: "UserInfo",
        component: () => import("../views/UserInfo.vue")
    },
    {
        meta: {
            title: "报表详情",
            keepAlive: true
        },
        path: "/CodeInfo/:submit_time(\\d{4}-\\d{2}-\\d{2})/:wait/:remove/:transit/:success/:back",
        name: "CodeInfo",
        component: () => import("../views/CodeInfo.vue")
    },
    {
        meta: {
            title: "直播间数据",
            keepAlive: true
        },
        path: "/Room/",
        name: "Room",
        component: () => import("../views/Room.vue")
    },
    {
        meta: {
            title: "热卖跟踪",
            keepAlive: true
        },
        path: "/Tracking/",
        name: "Tracking",
        component: () => import("../views/Tracking.vue")
    },
    {
        meta: {
            title: "选款购物车",
            keepAlive: true
        },
        path: "/Cart/:cart_name",
        name: "Cart",
        component: () => import("../views/Cart.vue")
    },
    {
        meta: {
            title: "VIP用户",
            keepAlive: true
        },
        path: "/VipUser/",
        name: "VipUser",
        component: () => import("../views/VipUser.vue")
    },
    {
        meta: {
            title: "直播间后台",
            keepAlive: true
        },
        path: "/RoomBack/:room_name",
        name: "RoomBack",
        component: () => import("../views/RoomBack.vue")
    },
    {
        meta: {
            title: "全量表款号信息",
            keepAlive: true
        },
        path: "/CodeCommodity/",
        name: "CodeCommodity",
        component: () => import("../views/CodeCommodity.vue")
    },
    {
        meta: {
            title: "新款状态",
            keepAlive: true
        },
        path: "/StyleStatus/",
        name: "StyleStatus",
        component: () => import("../views/StyleStatus.vue")
    },
    {
        meta: {
            title: "新款状态跟踪",
            keepAlive: true
        },
        path: "/NewStyleTracking/",
        name: "NewStyleTracking",
        component: () => import("../views/NewStyleTracking.vue")
    },
    {
        meta: {
            title: "测试",
            keepAlive: true
        },
        path: "/testdemo/",
        name: "testdemo",
        component: () => import("../views/TestDemo.vue")
    },
    {
        meta: {
            title: "标签库",
            keepAlive: true
        },
        path: "/tags/",
        name: "tags",
        component: () => import("../views/Tags.vue")
    },
    {
        meta: {
            title: "标签库",
            keepAlive: true
        },
        path: "/tagsphone/:name",
        name: "tags2",
        component: () => import("../views/TagsPhone.vue")
    },
    {
        meta: {
            title: "设计",
            keepAlive: true
        },
        path: "/design/",
        name: "design",
        component: () => import("../views/Design.vue")
    },
    {
        meta: {
            title: "设计2",
            keepAlive: true
        },
        path: "/design2/",
        name: "design2",
        component: () => import("../views/Design2.vue")
    },
    {
        meta: {
            title: "设计3",
            keepAlive: true
        },
        path: "/design3/:code/:name",
        name: "design3",
        component: () => import("../views/Design3.vue")
    },
    {
        meta: {
            title: "设计4",
            keepAlive: true
        },
        path: "/design4/:type/:name",
        name: "design4",
        component: () => import("../views/Design4.vue")
    },
    {
        meta: {
            title: "在线观众",
            keepAlive: true
        },
        path: "/roomphone/",
        name: "roomphone",
        component: () => import("../views/RoomLivePhone.vue")
    },
    {
        meta: {
            title: "在线观众",
            keepAlive: true
        },
        path: "/roomphone2/",
        name: "roomphone2",
        component: () => import("../views/RoomLivePhone2.vue")
    },
    {
        meta: {
            title: "设计",
            keepAlive: true
        },
        path: "/phonedesign/:name",
        name: "phonedesign",
        component: () => import("../views/PhoneDesign.vue")
    },
    {
        meta: {
            title: "详情",
            keepAlive: true
        },
        path: "/phonedesign/info/:code",
        name: "phonedesigninfo",
        component: () => import("../views/PhoneDesignInfo.vue")
    },
]

// 路由对象实例化
const router = createRouter({
    // history, 指定路由的模式
    history: createWebHistory(),
    // 路由列表
    routes,
});
router.beforeEach((to, from, next) => {
    const title = to.meta.title; // 获取目标路由的标题
    if (title) {
        document.title = title; // 更新页面标题
    }
    next(); // 继续导航
});

// 暴露路由对象
export default router