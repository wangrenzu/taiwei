<template>
  <el-upload
      class="upload-demo"
      drag
      action="http://192.168.1.137:8000/home/updateRepeatOrder/"
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
  home.show_update_repeat_order = false
  home.size = 20
  home.buttonType12 = 'success'
  home.putUpdateStatus(12).then(response=>{
    console.log(response)
  }).catch(err=>{
    console.log(err)
  })
  ElMessage(res)
}
const error = (err) => {
  ElMessage(err)
  console.log(err)
}

</script>

<style scoped>

</style>