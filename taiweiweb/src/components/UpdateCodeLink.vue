<template>
  <el-upload
      class="upload-demo"
      drag
      action="http://192.168.1.137:8000/cart/updateCodeLink/"
      name='excel-file'
      multiple
      :on-success="success"
      :on-error="error"
  >
    <el-icon class="el-icon--upload">
      <upload-filled/>
    </el-icon>
    <div class="el-upload__text">
      请上传要更新的excel <em>click to upload</em>
    </div>
  </el-upload>
</template>

<script setup>
import {ElMessage} from 'element-plus'
import * as XLSX from "xlsx";
import cart from "../api/cart.js";
import FileSaver from 'file-saver';



const cart_link = [
  {key: 'code', label: '款号'},
  {key: 'link', label: '链接'},
]
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

const success = (response) => {
  exportExcel(cart_link, response)
  cart.update_code = false
}
const error = (err) => {
  ElMessage(err)
  console.log(err)
}

</script>

<style scoped>

</style>