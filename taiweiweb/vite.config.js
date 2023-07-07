import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  server: {
    host: '192.168.1.137'
  },
  plugins: [
    vue({
      styleImport: {
        // 添加下面这行代码，指定 element-plus 的 SCSS 文件路径
        // 根据你的项目结构调整路径，如果有必要
        include: /element-plus[\\/]lib[\\/]theme-chalk[\\/]index\.css/
      }
    }),
    Components({
      resolvers: [ElementPlusResolver()],
      dts: true,
      importStyle: 'sass'
    }),
  ]
})
