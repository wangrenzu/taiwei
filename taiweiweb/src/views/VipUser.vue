<template>


  <el-table :data="home.vipUser_list" style="width: 100%" border fit>
    <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
    <el-table-column prop="name" label="名字" width="100" show-overflow-tooltip/>
    <el-table-column fixed="right" label="删除" width="80">
      <template #default="scope">
        <el-button
            link
            type="primary"
            size="small"
            @click.prevent="delVipUser(scope.row.name)"
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


// 获取所有的vip用户
const getVipUser = () => {
  home.getVipUser().then(response => {
    console.log(response)
    home.vipUser_list = response.data.original_data
  }).catch(err => {
    ElMessage(err)
  })
}
getVipUser()


// 根据名字删除vip用户
const delVipUser = (name)=>{
  home.delVipUser(name).then(response => {
    ElMessage("删除成功")
    getVipUser()
  }).catch(err => {
    ElMessage(err)
  })
}

</script>

<style scoped>

</style>