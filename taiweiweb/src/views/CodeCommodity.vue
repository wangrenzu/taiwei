<template>


  <el-input v-model="code" style="width: 200px"
            placeholder="请输入款号" clearable></el-input>


  <el-date-picker
        v-model="data_time"
        type="date"
        placeholder="请选择起始日期"
    />
  <el-button type="primary" @click="getCodeInfo">搜索</el-button>
  <br>
  <span v-if="date2">
    库存：{{date2[4]}} 订购量: {{date2[5]}} 待退货: {{date2[1]}} 待收退货: {{date2[2]}}
    预计可卖量：{{date2[1] + date2[2] + date2[4] - date2[5]}}
    裁床：{{date3[1]}} 车间：{{date3[2]}} 后道：{{date3[3]}}
  </span>
  <el-table v-if="codeInfo" :data="codeInfo" style="width: 100%" border fit height="800">
    <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
    <el-table-column prop="date_time" label="日期" width="120" sortable show-overflow-tooltip/>
    <el-table-column prop="code" label="款号" width="100" sortable show-overflow-tooltip/>
    <el-table-column prop="live_deal_item_count" label="全量表销量" width="80" sortable show-overflow-tooltip/>
    <el-table-column prop="live_exposure_count" label="全量表曝光" width="90" sortable show-overflow-tooltip/>
    <el-table-column prop="live_click_count" label="曝光点击率" width="90" sortable show-overflow-tooltip>
      <template #default="score">
        {{(score.row.live_click_count*100).toFixed(2)+'%'}}
      </template>
    </el-table-column>
    <el-table-column prop="live_deal_user_count" label="点击成交率" width="70" sortable show-overflow-tooltip>
      <template #default="score">
        {{(score.row.live_deal_user_count*100).toFixed(2)+'%'}}
      </template>
    </el-table-column>
    <el-table-column prop="success_num" label="成功" width="70" sortable show-overflow-tooltip/>
    <el-table-column prop="success_num" label="成功率" width="70" sortable show-overflow-tooltip>
      <template #default="score">
        {{score.row.live_deal_item_count ? ((score.row.success_num / score.row.live_deal_item_count)*100).toFixed(2)+'%' :''}}
      </template>
    </el-table-column>
    <el-table-column prop="pending_num" label="待发" width="70" sortable show-overflow-tooltip/>
    <el-table-column prop="transit_num" label="在途" width="70" sortable show-overflow-tooltip/>
    <el-table-column prop="back_num" label="退回" width="70" sortable show-overflow-tooltip/>
    <el-table-column prop="liev_success_num" label="千川成功" sortable width="70" show-overflow-tooltip/>
  </el-table>
</template>

<script setup>

import home from "../api/home.js";
import {ref} from "vue";

let codeInfo = ref()
let code = ref()
let data_time = ref()
let date2 = ref()
let date3 = ref()
const getCodeInfo = () => {
  // 获取当前时间
  const currentTime = new Date(data_time.value);

  // 转换为中国时区
  const options = { timeZone: 'Asia/Shanghai' };
  const chinaTime = currentTime.toLocaleString('en-US', options);


  // 格式化日期
  const year = currentTime.getFullYear();
  const month = (currentTime.getMonth() + 1).toString().padStart(2, '0');
  const day = currentTime.getDate().toString().padStart(2, '0');
  const formattedDate = `${year}-${month}-${day}`;

  home.searchCodeInfo(code.value,formattedDate).then(response => {
    date3.value = response.data.message.data3[0]
    date2.value = response.data.message.data2[0]
    codeInfo.value =  response.data.message.data1.map(item => {
      return {
        date_time: item[0],
        code: item[1],
        live_deal_item_count: item[2],
        live_exposure_count: item[3],
        live_click_count: item[4],
        live_deal_user_count: item[5],
        success_num: item[6],
        pending_num: item[7],
        transit_num: item[8],
        back_num: item[9],
        liev_success_num: item[10]
      }
    })
  }).catch(err => {
    console.log(err)
  })
}



</script>

<style scoped>

</style>