<template>

  <el-input v-model="home.addCode" style="width: 200px" placeholder="请输入要跟踪的款号" clearable></el-input>
  <el-button type="primary" @click="addTracking">添加</el-button>
  <el-button type="primary" @click="refresh">刷新</el-button>
  <el-table :data="home.tracking_data" v-loading="home.loading" style="width: 100%" height="800" border fit>
    <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
    <el-table-column prop="code" label="款号" width="100" show-overflow-tooltip/>
    <el-table-column prop="name" label="货品名称" width="100" show-overflow-tooltip/>
    <el-table-column label="图片" width="120">
      <template #default="scope">
        <el-image style="width: 90px; height: 100px"
                  :src="scope.row.image"/>
      </template>
    </el-table-column>
    <el-table-column prop="order_quantity" label="订购量" width="80" sortable show-overflow-tooltip/>
    <el-table-column prop="cutting_quantity" label="裁床" width="60" show-overflow-tooltip/>
    <el-table-column prop="workshop_quantity" label="车间" width="60" show-overflow-tooltip/>
    <el-table-column prop="rear_quantity" label="后道" width="60" show-overflow-tooltip/>
    <el-table-column prop="taiwei_quantity" label="泰维" width="60" show-overflow-tooltip/>
    <el-table-column prop="yifa_quantity" label="意法" width="60" show-overflow-tooltip/>
    <el-table-column prop="moya_quantity" label="茉雅" width="60" show-overflow-tooltip/>
    <el-table-column prop="live_exposure_count" label="直播间曝光" width="100" show-overflow-tooltip/>
    <el-table-column prop="live_deal_item_count" label="30天成交" width="90" show-overflow-tooltip/>
    <el-table-column prop="cancelled_quantity" label="取消" width="60" show-overflow-tooltip/>
    <el-table-column prop="pending_shipment_quantity" label="待发+在途" width="95" show-overflow-tooltip/>
    <el-table-column prop="successful_quantity" label="成功" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="returned_quantity" label="退回" width="60" sortable show-overflow-tooltip/>
    <el-table-column fixed="right" label="删除" width="80">
      <template #default="scope">
        <el-button
            link
            type="primary"
            size="small"
            @click.prevent="delTracking(scope.row.id)"
        >
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>

import home from "../api/home.js";
import {ElMessage} from "element-plus";
import {watch} from "vue";


// 获取所有款号跟踪信息
const getTrakcing = () => {
  home.getTrakcing().then(response => {
    home.tracking_data = response.data
    home.loading = false
  }).catch(err => {
    console.log(err)
  })
}
getTrakcing()


// 删除某个款号信息
const delTracking = (id) => {
  home.delTrakcing(id).then(response => {
    ElMessage('删除成功')
    getTrakcing()
  }).catch(err => {
    console.log(err)
    ElMessage(err)
  })
}

// 添加款号到款号追踪中
const addTracking = () => {
  home.addTracking().then(response => {
    ElMessage('添加成功')
    getTrakcing()
  }).catch(err => {
    console.log(err)
    ElMessage(err)
  })
}
// 刷新状态和信息
const refresh = () => {
  home.code_list = []
  home.tracking_data.forEach(item => {
    home.code_list.push(item.code)
  })
  home.refreshTracking().then(response => {
    getTrakcing()
  }).catch(err => {
    console.log(err)
  })
}


</script>

<style scoped>

</style>