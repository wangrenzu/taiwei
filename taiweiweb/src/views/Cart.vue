<template>


  <el-input v-model="cart.cart_code" style="width: 200px"
            placeholder="请输入款号" clearable></el-input>
  <el-button type="primary" @click="addCart">加入购物车</el-button>
  <el-button type="primary" @click="getCartLink">导出链接

    <el-icon class="el-icon--right">
      <Download/>
    </el-icon>
  </el-button>
  <el-button type="primary" @click="addDesignCode">设计</el-button>
  <el-button type="primary" @click="cart.update_code=true">上传导出
    <el-icon class="el-icon--right">
      <Download/>
    </el-icon>
  </el-button>

  <el-dialog :width="600" v-model="cart.update_code">
    <UpdateCodeLink></UpdateCodeLink>
  </el-dialog>


  <br>
  <el-button type="primary" @click="exportExcel(cartData,cart.cart_list)">导出
    <el-icon class="el-icon--right">
      <Download/>
    </el-icon>
  </el-button>
  <el-button type="primary" @click="refresh">刷新</el-button>
  <span>{{ route.params.cart_name }}</span>
  <el-table :data="cart.cart_list" style="width: 100%" border fit height="800">
    <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
    <el-table-column prop="commodity_code" label="款号" width="80" show-overflow-tooltip/>
    <el-table-column prop="price" label="单价" width="70" show-overflow-tooltip/>
    <el-table-column prop="product_name" label="货品名" width="100" show-overflow-tooltip/>
    <el-table-column label="图片" width="100">
      <template #default="scope">
        <el-image style="width: 90px; height: 100px"
                  :src="'http://192.168.1.233/web_images/' + scope.row.commodity_code + '.jpg'">
        </el-image>
      </template>
    </el-table-column>
    <el-table-column prop="order_quantity" label="订购量" width="50" show-overflow-tooltip/>
    <el-table-column prop="workshop_quantity" label="车间规格量" width="80" show-overflow-tooltip/>
    <el-table-column prop="workshop_quantity_num" label="可卖量" width="80" show-overflow-tooltip/>
    <el-table-column prop="post_processing_quantity" label="后道规格量" width="80" show-overflow-tooltip/>
    <el-table-column prop="post_processing_quantity_num" label="可卖量" width="80" show-overflow-tooltip/>
    <el-table-column prop="taiwei_yifa_moyajia_quantity" label="泰维+意法+茉雅规格量" width="80"
                     show-overflow-tooltip/>
    <el-table-column prop="taiwei_yifa_moyajia_quantity_num" label="可卖量" width="80" show-overflow-tooltip/>
    <el-table-column prop="pending_and_in_transit" label="待发+在途" width="60" show-overflow-tooltip/>
    <el-table-column prop="cancelled" label="取消" width="60" show-overflow-tooltip/>
    <el-table-column prop="successful" label="成功" width="60" show-overflow-tooltip/>
    <el-table-column prop="returned" label="退回" width="60" show-overflow-tooltip/>

    <el-table-column prop="live_deal_conversion_rate" label="直播间30天最大转化率" width="100" sortable show-overflow-tooltip>
      <template #default="scope">
        {{ (scope.row.live_deal_conversion_rate * 100).toFixed(2) + '%' }}
      </template>
    </el-table-column>
    <el-table-column  prop="exposure_click_rate" label="曝光点击率" width="100" sortable show-overflow-tooltip>
      <template #default="scope">
        {{ (scope.row.exposure_click_rate * 100).toFixed(2) + '%' }}
      </template>
    </el-table-column>
    <el-table-column prop="max_exposure_quantity" label="近三天最大曝光量" sortable width="80" show-overflow-tooltip/>
    <el-table-column prop="avg_live_exposure_count" label="3天平均曝光量" sortable width="80" show-overflow-tooltip/>
    <el-table-column prop="exposure" label="本场曝光量" sortable width="80" show-overflow-tooltip/>
    <el-table-column prop="clickExposure" label="本场曝光点击率" sortable  width="80" show-overflow-tooltip>
      <template #default="scope">
        {{ (scope.row.clickExposure * 100).toFixed(2) + '%' }}
      </template>
    </el-table-column>
    <el-table-column  prop="clickDeal" label="本场点击成交率" sortable width="80" show-overflow-tooltip>
      <template #default="scope">
        {{ (scope.row.clickDeal * 100).toFixed(2) + '%' }}
      </template>
    </el-table-column>
    <el-table-column prop="prediction" label="预测销量" width="60" show-overflow-tooltip/>
    <el-table-column prop="prediction_money" label="预测金额" width="70" show-overflow-tooltip/>
    <el-table-column prop="source" label="来源" width="70" show-overflow-tooltip/>

    <el-table-column fixed="right" label="删除" width="80">
      <template #default="scope">
        <el-button
            link
            type="primary"
            size="small"
            @click.prevent="delCart(scope.row.id)"
        >
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>


import cart from "../api/cart.js";
import {ElMessage} from "element-plus";
import * as XLSX from "xlsx";
import FileSaver from 'file-saver';
import {Download} from '@element-plus/icons-vue'
import {useRoute, useRouter} from 'vue-router';
import UpdateCodeLink from "../components/UpdateCodeLink.vue";
import {useCounterStore} from "../stores/store.js";


const route = useRoute();
const router = useRouter();

// 导出的字段内容
const cartData = [
  {key: 'commodity_code', label: '款号'},
  {key: 'product_name', label: '货品名'},
  {key: 'image', label: '图片'},
  {key: 'order_quantity', label: '订购量'},
  {key: 'workshop_quantity', label: '车间规格量'},
  {key: 'workshop_quantity_num', label: '可卖量'},
  {key: 'post_processing_quantity', label: '后道规格量'},
  {key: 'post_processing_quantity_num', label: '可卖量'},
  {key: 'taiwei_yifa_moyajia_quantity', label: '泰维+意法+茉雅规格量'},
  {key: 'taiwei_yifa_moyajia_quantity_num', label: '可卖量'},
  {key: 'pending_and_in_transit', label: '待发+在途'},
  {key: 'cancelled', label: '取消'},
  {key: 'successful', label: '成功'},
  {key: 'returned', label: '退回'},
  {key: 'price', label: '金额'},
  {key: 'live_deal_conversion_rate', label: '直播间成交转化率'},
  {key: 'exposure_click_rate', label: '曝光点击率'},
  {key: 'max_exposure_quantity', label: '最大曝光量'},
  {key: 'avg_live_exposure_count', label: '3天平均曝光量'},
  {key: 'prediction', label: '预测销量'},
  {key: 'prediction_money', label: '预测金额'},
  {key: 'exposure', label: '本场曝光量'},
  {key: 'clickExposure', label: '本场曝光点击率'},
  {key: 'clickDeal', label: '本场点击成交率'},
]
const cart_link = [
  {key: 'code', label: '款号'},
  {key: 'link', label: '链接'},
]

//导出到excel
const exportExcel = (exportFields, data_list) => {
  const sheet = XLSX.utils.json_to_sheet(data_list.map(item => {
    const row = {};
    exportFields.forEach(field => {
      row[field.label] = item[field.key];
    });
    return row;
  }));
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, sheet, 'Sheet1');
  const filename = 'table.xlsx';
  const wbout = XLSX.write(workbook, {bookType: 'xlsx', type: 'array'});
  const blob = new Blob([wbout], {type: 'application/octet-stream'});
  FileSaver.saveAs(blob, filename);
}

// 获取购物车信息
const getCart = () => {
  const cart_name = route.params.cart_name
  cart.getCart(cart_name).then(response => {
    cart.cart_list = response.data
  }).catch(err => {
    console.log(err)
  })

}
getCart()


// 把某个商品从购物车中删除
const delCart = (id) => {
  cart.delCart(id).then(response => {
    ElMessage({
      message: "删除成功",
      type: 'success',
    })
    getCart()
  }).catch(err => {
    ElMessage.error("添加失败")
  })
}

// 刷新购物车状态
const refresh = () => {
  cart.code_list = {}
  cart.cart_list.forEach(item => {
    cart.code_list[item.commodity_code] = item.cart_name + '/' + item.source;
  })
  cart.refreshCart().then(response => {
    getCart()
    ElMessage({
      message: "刷新成功",
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error("刷新失败")
  })
}


// 添加商品到购物车
const addCart = () => {
  if (cart.cart_code === null) {
    alert("请输入款号")
    return
  }
  cart.addCart(cart.cart_code, route.params.cart_name, route.params.cart_name).then(response => {
    ElMessage({
      message: "添加成功",
      type: 'success',
    })
    getCart()
  }).catch(err => {
    ElMessage.error("添加失败")
  })
}

const getCartLink = () => {
  cart.codes = []
  cart.cart_list.forEach(item => {
    cart.codes.push(item.commodity_code)
  })
  cart.getCartLink().then(response => {
    exportExcel(cart_link, response.data)
  }).catch(err => {
    console.log(err)
  })
}
const store = useCounterStore()
const addDesignCode = () => {
  cart.codes = []
  cart.cart_list.forEach(item => {
    cart.codes.push(item.commodity_code)
  })
  cart.addDesign(cart.codes).then(response => {
    store.code_list = cart.codes
    router.push({ path: '/design/'  });
  }).catch(err => {
    ElMessage.error("错误")
  })
}

</script>

<style scoped>

</style>