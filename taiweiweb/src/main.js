import {createApp} from 'vue'
import App from './App.vue'
import router from "./router/index.js";
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import {createPinia} from 'pinia'

const pinia = createPinia()
const app = createApp(App);

app.use(router);
app.use(ElementPlus, {locale: zhCn});
app.use(pinia)

app.mount('#app');