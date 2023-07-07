<template>
  <el-upload
      class="upload-demo"
      drag
      action="http://192.168.1.137:8000/home/updateOneCommodity/"
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
import home from "../api/home.js";

const success = (res) => {
  home.show_update_onecommodity = false
  home.size = 20
  home.buttonType6 = 'success'
  home.putUpdateStatus(6).then(response=>{
  }).catch(err=>{
    console.log(err)
  })
  ElMessage({
    message: res.message,
    type: 'success',
  })
}
const error = (err) => {
  ElMessage.error(err)
}
</script>

<style scoped>

</style>