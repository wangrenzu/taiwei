import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from 'unplugin-vue-components/resolvers'

export default defineConfig({
    server:{
      host:'192.168.1.137'
    },
    plugins: [
        vue(),
        Components({
            resolvers: [ElementPlusResolver()],
        }),

    ]
})
