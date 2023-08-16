<template>

  <el-input v-model="code"
            type="textarea"
            style="width: 200px"
            placeholder="请输入款号" clearable></el-input>
  <el-button type="primary" @click="getStyleStatus">
    搜索
    <el-icon color="white" class="el-icon--right">
      <Search/>
    </el-icon>
  </el-button>
  <el-button type="primary" @click="exportExcel(Fields)">
    导出
    <el-icon color="white" class="el-icon--right">
      <Download/>
    </el-icon>
  </el-button>
  <el-table :data="home.style_status_list" v-loading="loading" style="width: 100%" height="800" border fit>
    <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
    <el-table-column prop="date_time" label="新款下单日期" width="110" show-overflow-tooltip/>
    <el-table-column prop="repeat_count" label="翻单次数" width="90" show-overflow-tooltip/>
    <el-table-column prop="code" label="款号" width="100" show-overflow-tooltip/>
    <el-table-column prop="cai_chuang" label="裁床" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="che_jian" label="车间" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="hou_dao" label="后道" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="tai_wei" label="泰维" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="yi_fa" label="意法" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="mo_ya" label="茉雅" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="fabric_price" label="面料总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="materials_price" label="辅料总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="factory_price" label="工厂总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="salesrecord_price" label="档口总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="order_price" label="订单总金额" width="120" sortable show-overflow-tooltip/>
    <el-table-column prop="to_salesrecord_time" label="最近到档口时间" width="120" sortable show-overflow-tooltip/>
    <el-table-column prop="back_rate" label="退货损耗" width="110" sortable show-overflow-tooltip/>
  </el-table>
</template>

<script setup>

import home from "../api/home.js";
import {ElInput} from 'element-plus'
import {Search, Download} from '@element-plus/icons-vue'
import {nextTick, ref, watch} from "vue";
import * as XLSX from "xlsx";
import FileSaver from 'file-saver';


// 款号
const code = ref('')

const loading = ref(false)


// 导出的字段
const Fields = [
  {key: 'date_time', label: '新款下单日期'},
  {key: 'repeat_count', label: '翻单次数'},
  {key: 'code', label: '款号'},
  {key: 'cai_chuang', label: '裁床'},
  {key: 'che_jian', label: '车间'},
  {key: 'hou_dao', label: '后道'},
  {key: 'tai_wei', label: '泰维'},
  {key: 'yi_fa', label: '意法'},
  {key: 'mo_ya', label: '茉雅'},
  {key: 'fabric_price', label: '面料总金额'},
  {key: 'materials_price', label: '辅料总金额'},
  {key: 'factory_price', label: '工厂总金额'},
  {key: 'salesrecord_price', label: '档口总金额'},
  {key: 'order_price', label: '订单总金额'},
  {key: 'to_salesrecord_time', label: '最近到档口时间'},
  {key: 'back_rate', label: '退货损耗'},

];
// 导出内容到excel
const exportExcel = (exportFields) => {
  const sheet = XLSX.utils.json_to_sheet(home.style_status_list.map(item => {
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

// 根据筛选条件获取内容
const getStyleStatus = () => {
  loading.value = true
  home.styleTracing(code.value).then(response => {
    home.style_status_list = response.data
    loading.value = false
  }).catch(err => {
    console.log(err)
  })
}


</script>

<style scoped>

</style>